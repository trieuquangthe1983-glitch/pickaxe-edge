"""Reddit source — all tests use injected fake fetch (no network)."""

from data.reddit_source import (
    NICHE_SUBREDDITS,
    refresh_reddit_signals,
    replace_reddit_signals,
    search_reddit,
)
from data.sources import get_signals


def _fake_fetch_factory(payload: dict | None):
    """Returns a fetch function that always returns the given payload."""
    def _fetch(url: str) -> dict:
        if payload is None:
            raise RuntimeError("forced failure")
        return payload
    return _fetch


def _payload(posts: list[dict]) -> dict:
    return {"data": {"children": [{"data": p} for p in posts]}}


def test_search_reddit_returns_none_for_unknown_niche():
    sig = search_reddit("does_not_exist", "x", fetch=_fake_fetch_factory(_payload([])))
    assert sig is None


def test_search_reddit_returns_none_when_no_posts():
    fake = _fake_fetch_factory(_payload([]))
    sig = search_reddit("crypto_trading", "btc etf", fetch=fake)
    assert sig is None


def test_search_reddit_aggregates_multiple_subs():
    """3 subs in crypto_trading -> fake fetch called 3 times, 6 posts aggregated."""
    payload = _payload([
        {"score": 1000, "num_comments": 200, "author": "alice", "title": "etf news"},
        {"score": 500,  "num_comments": 50,  "author": "bob",   "title": "etf flow"},
    ])
    fake = _fake_fetch_factory(payload)
    sig = search_reddit("crypto_trading", "btc etf", fetch=fake)
    assert sig is not None
    assert sig.platform == "reddit"
    assert sig.niche == "crypto_trading"
    assert sig.sample_size == 6   # 2 posts * 3 subs
    assert sig.supply_count == 2  # unique authors across all subs
    assert 0.0 < sig.engagement_score <= 1.0


def test_search_reddit_filters_bot_authors():
    payload = _payload([
        {"score": 100, "num_comments": 5, "author": "real_user"},
        {"score": 50,  "num_comments": 2, "author": "AutoModerator"},
        {"score": 30,  "num_comments": 1, "author": "[deleted]"},
    ])
    fake = _fake_fetch_factory(payload)
    sig = search_reddit("longevity", "rapamycin", fetch=fake)
    assert sig is not None
    assert sig.supply_count == 1  # only real_user counts


def test_search_reddit_tolerates_fetch_failure_on_some_subs():
    """One sub fails, others succeed -> still get aggregated signal."""
    call_count = [0]
    payload = _payload([{"score": 200, "num_comments": 40, "author": "u1"}])
    def flaky(url: str):
        call_count[0] += 1
        if call_count[0] == 1:
            raise RuntimeError("network error on first sub")
        return payload
    sig = search_reddit("indie_saas", "pricing", fetch=flaky)
    assert sig is not None
    # 3 subs, 1 failed -> 2 successful, 1 post each = sample_size 2
    assert sig.sample_size == 2


def test_engagement_scales_with_score():
    low_payload = _payload([{"score": 5,    "num_comments": 1,   "author": "u1"}])
    hi_payload  = _payload([{"score": 5000, "num_comments": 500, "author": "u1"}])
    low = search_reddit("crypto_trading", "x", fetch=_fake_fetch_factory(low_payload))
    hi  = search_reddit("crypto_trading", "x", fetch=_fake_fetch_factory(hi_payload))
    assert hi.engagement_score > low.engagement_score


def test_refresh_reddit_signals_handles_empty_topic_list():
    assert refresh_reddit_signals("crypto_trading", [], fetch=_fake_fetch_factory(_payload([]))) == []


def test_refresh_reddit_signals_skips_topics_with_no_results():
    """Topics returning no posts shouldn't appear in output."""
    def fake(url: str):
        if "good+topic" in url:
            return _payload([{"score": 100, "num_comments": 10, "author": "u1"}])
        return _payload([])
    sigs = refresh_reddit_signals("crypto_trading", ["good topic", "empty"], fetch=fake)
    assert len(sigs) == 1
    assert sigs[0].topic == "good topic"


def test_replace_reddit_signals_swaps_only_matching_topics():
    base = get_signals("crypto_trading")
    # build a single live signal for an existing topic
    live = [s for s in base if s.platform == "reddit"][:1]
    if not live:
        return  # nothing to swap
    target_topic = live[0].topic
    # make a "live" version with very different numbers
    from core.types import PlatformSignal
    fake_live = [PlatformSignal(
        platform="reddit", niche="crypto_trading",
        topic=target_topic, engagement_score=0.99,
        supply_count=999, sample_size=999,
    )]
    out = replace_reddit_signals(base, fake_live, "crypto_trading")
    swapped = [s for s in out if s.platform == "reddit" and s.topic == target_topic][0]
    assert swapped.engagement_score == 0.99
    assert swapped.supply_count == 999
    # Non-reddit signals untouched
    yt_count_before = sum(1 for s in base if s.platform == "youtube")
    yt_count_after  = sum(1 for s in out if s.platform == "youtube")
    assert yt_count_before == yt_count_after


def test_all_seed_niches_have_subreddit_mappings():
    from data.sources import list_niches
    for niche in list_niches():
        assert niche in NICHE_SUBREDDITS, f"missing subreddit mapping for {niche}"
        assert NICHE_SUBREDDITS[niche], f"empty subreddit list for {niche}"
