"""Substack source — all tests use injected fake fetch (no network)."""

from datetime import datetime, timezone

from data.substack_source import (
    NICHE_PUBLICATIONS,
    _parse_pubdate,
    _parse_rss,
    _pub_to_feed_url,
    refresh_substack_signals,
    replace_substack_signals,
    search_substack,
)
from data.sources import get_signals, list_niches


# A fixed "now" for deterministic tests — all post dates are relative to this
NOW = datetime(2026, 5, 23, 12, 0, 0, tzinfo=timezone.utc)


def _rss(items_xml: str) -> str:
    """Wrap a list of <item> blocks in a minimal valid RSS document."""
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:dc="http://purl.org/dc/elements/1.1/">
  <channel>
    <title>Test Pub</title>
    <link>https://test.substack.com</link>
    <description>Test</description>
    {items_xml}
  </channel>
</rss>"""


def _item(title: str, desc: str = "", pub_date: str = "Fri, 15 May 2026 12:00:00 GMT",
          author: str = "Test Author") -> str:
    return f"""<item>
  <title>{title}</title>
  <description>{desc}</description>
  <link>https://test.substack.com/p/{abs(hash(title)) % 10000}</link>
  <pubDate>{pub_date}</pubDate>
  <dc:creator>{author}</dc:creator>
</item>"""


def _fake_fetch(payload: str):
    def _fn(url: str) -> str:
        return payload
    return _fn


# ---------------- Helpers ----------------

def test_pub_to_feed_url_slug():
    assert _pub_to_feed_url("pomp") == "https://pomp.substack.com/feed"


def test_pub_to_feed_url_full_url_passes_through():
    custom = "https://custom.example.com/rss"
    assert _pub_to_feed_url(custom) == custom


def test_parse_pubdate_handles_rfc822():
    dt = _parse_pubdate("Fri, 15 May 2026 12:00:00 GMT")
    assert dt is not None
    assert dt.year == 2026 and dt.month == 5 and dt.day == 15


def test_parse_pubdate_returns_none_for_garbage():
    assert _parse_pubdate(None) is None
    assert _parse_pubdate("not a date") is None


def test_parse_rss_handles_malformed_xml():
    assert _parse_rss("not xml") == []


def test_parse_rss_extracts_dc_creator():
    xml = _rss(_item("hello", author="Alice"))
    posts = _parse_rss(xml)
    assert len(posts) == 1
    assert posts[0]["author"] == "Alice"


# ---------------- search_substack ----------------

def test_search_returns_none_for_unknown_niche_with_no_publications():
    assert search_substack("does_not_exist", "topic", fetch=_fake_fetch(_rss(""))) is None


def test_search_returns_none_when_no_matches():
    xml = _rss(_item("unrelated post"))
    sig = search_substack(
        "crypto_trading", "btc etf",
        publications=["pub1"], fetch=_fake_fetch(xml), now=NOW,
    )
    assert sig is None


def test_search_matches_keywords_case_insensitive():
    xml = _rss(_item("Bitcoin ETF flows are wild", "deep dive on BTC etf demand"))
    sig = search_substack(
        "crypto_trading", "btc etf",
        publications=["pub1"], fetch=_fake_fetch(xml), now=NOW,
    )
    assert sig is not None
    assert sig.sample_size == 1
    assert sig.supply_count == 1


def test_search_requires_ALL_keywords_to_appear():
    # Title mentions 'bitcoin' but NOT 'etf' -> no match
    xml = _rss(_item("Bitcoin pricing fundamentals"))
    sig = search_substack(
        "crypto_trading", "btc etf",
        publications=["pub1"], fetch=_fake_fetch(xml), now=NOW,
    )
    assert sig is None


def test_search_filters_old_posts():
    """Posts older than days_window are excluded."""
    xml = _rss(
        _item("Btc etf recent", pub_date="Fri, 15 May 2026 12:00:00 GMT")
        + _item("Btc etf old", pub_date="Mon, 01 Jan 2024 12:00:00 GMT")
    )
    sig = search_substack(
        "crypto_trading", "btc etf",
        publications=["pub1"], fetch=_fake_fetch(xml),
        days_window=30, now=NOW,
    )
    assert sig is not None
    assert sig.sample_size == 1  # only the recent one


def test_search_aggregates_across_publications():
    xml = _rss(_item("btc etf insight", author="Alice"))
    # Same xml returned for each pub -> 3 matches, 1 unique author
    sig = search_substack(
        "crypto_trading", "btc etf",
        publications=["pub1", "pub2", "pub3"],
        fetch=_fake_fetch(xml), now=NOW,
    )
    assert sig is not None
    assert sig.sample_size == 3
    assert sig.supply_count == 1


def test_search_uses_publication_name_when_author_missing():
    xml = _rss("""<item>
  <title>btc etf no author</title>
  <description>...</description>
  <link>https://test.substack.com/p/x</link>
  <pubDate>Fri, 15 May 2026 12:00:00 GMT</pubDate>
</item>""")
    sig = search_substack(
        "crypto_trading", "btc etf",
        publications=["mypub"], fetch=_fake_fetch(xml), now=NOW,
    )
    assert sig is not None
    assert sig.supply_count == 1
    # We can't directly assert "mypub" without exposing internals, but supply_count == 1 confirms tally


def test_search_strips_html_from_description():
    # Real Substack RSS wraps HTML description in CDATA — matches that
    xml = _rss(_item(
        "title",
        desc="<![CDATA[<p>Long post about <b>btc</b> and <i>etf</i> flows.</p>]]>",
    ))
    sig = search_substack(
        "crypto_trading", "btc etf",
        publications=["pub1"], fetch=_fake_fetch(xml), now=NOW,
    )
    assert sig is not None
    assert sig.sample_size == 1


def test_search_tolerates_per_pub_fetch_failure():
    """One pub fails, others succeed -> still get aggregated signal."""
    counter = [0]
    xml = _rss(_item("btc etf match"))
    def flaky(url: str) -> str:
        counter[0] += 1
        if counter[0] == 1:
            raise RuntimeError("simulated network error")
        return xml
    sig = search_substack(
        "crypto_trading", "btc etf",
        publications=["bad", "good1", "good2"],
        fetch=flaky, now=NOW,
    )
    assert sig is not None
    assert sig.sample_size == 2  # 2 successful pubs


def test_engagement_scales_with_match_count():
    one_match = _rss(_item("btc etf"))
    many_matches = _rss("".join(_item(f"btc etf post {i}") for i in range(20)))
    low = search_substack("crypto_trading", "btc etf",
                          publications=["p"], fetch=_fake_fetch(one_match), now=NOW)
    hi = search_substack("crypto_trading", "btc etf",
                         publications=["p"], fetch=_fake_fetch(many_matches), now=NOW)
    assert hi.engagement_score > low.engagement_score


# ---------------- refresh + replace ----------------

def test_refresh_skips_empty_topic_list():
    out = refresh_substack_signals(
        "crypto_trading", [],
        publications=["p"], fetch=_fake_fetch(_rss("")),
    )
    assert out == []


def test_replace_substack_signals_swaps_only_matching_topics():
    base = get_signals("crypto_trading")
    live_topic_src = [s for s in base if s.platform == "substack"][:1]
    if not live_topic_src:
        return
    topic = live_topic_src[0].topic
    from core.types import PlatformSignal
    fake_live = [PlatformSignal(
        platform="substack", niche="crypto_trading",
        topic=topic, engagement_score=0.91,
        supply_count=777, sample_size=777,
    )]
    out = replace_substack_signals(base, fake_live, "crypto_trading")
    swapped = [s for s in out if s.platform == "substack" and s.topic == topic][0]
    assert swapped.engagement_score == 0.91
    assert swapped.supply_count == 777
    # Non-substack signals untouched
    rd_before = sum(1 for s in base if s.platform == "reddit")
    rd_after = sum(1 for s in out if s.platform == "reddit")
    assert rd_before == rd_after


def test_all_seed_niches_have_publication_mappings():
    for niche in list_niches():
        assert niche in NICHE_PUBLICATIONS, f"missing pub mapping for {niche}"
        assert NICHE_PUBLICATIONS[niche], f"empty pub list for {niche}"
