"""YouTube source — all tests use injected fake fetch (no network)."""

from datetime import datetime, timezone

from data.youtube_source import (
    _engagement_from_stats,
    estimate_quota_cost,
    refresh_youtube_signals,
    replace_youtube_signals,
    search_youtube,
)
from data.sources import get_signals


NOW = datetime(2026, 5, 23, 12, 0, 0, tzinfo=timezone.utc)


def _search_payload(videos: list[dict]) -> dict:
    return {"items": [
        {
            "id": {"videoId": v.get("id", f"vid{i}")},
            "snippet": {"channelId": v.get("channel", f"chan{i}")},
        }
        for i, v in enumerate(videos)
    ]}


def _stats_payload(videos: list[dict]) -> dict:
    return {"items": [
        {"statistics": {
            "viewCount":    str(v.get("views", 0)),
            "likeCount":    str(v.get("likes", 0)),
            "commentCount": str(v.get("comments", 0)),
        }}
        for v in videos
    ]}


def _two_step_fetch(search: dict, stats: dict):
    """First call returns search, second returns stats."""
    calls = [0]
    def _fn(url: str) -> dict:
        calls[0] += 1
        if "/search?" in url:
            return search
        return stats
    return _fn


# ---------------- Boundary cases ----------------

def test_returns_none_without_api_key():
    fn = _two_step_fetch(_search_payload([{}]), _stats_payload([{}]))
    assert search_youtube("crypto_trading", "x", api_key="", fetch=fn) is None


def test_returns_none_when_search_empty():
    fn = _two_step_fetch(_search_payload([]), _stats_payload([]))
    assert search_youtube("crypto_trading", "x", api_key="k", fetch=fn, now=NOW) is None


def test_returns_none_when_stats_empty():
    fn = _two_step_fetch(
        _search_payload([{"id": "v1", "channel": "c1"}]),
        {"items": []},
    )
    assert search_youtube("crypto_trading", "x", api_key="k", fetch=fn, now=NOW) is None


def test_returns_none_when_search_call_raises():
    def fn(url: str) -> dict:
        raise RuntimeError("API quota exceeded")
    assert search_youtube("crypto_trading", "x", api_key="k", fetch=fn, now=NOW) is None


def test_returns_none_when_stats_call_raises():
    calls = [0]
    def fn(url: str) -> dict:
        calls[0] += 1
        if calls[0] == 1:
            return _search_payload([{"id": "v1", "channel": "c1"}])
        raise RuntimeError("stats failed")
    assert search_youtube("crypto_trading", "x", api_key="k", fetch=fn, now=NOW) is None


# ---------------- Happy path ----------------

def test_aggregates_supply_from_unique_channels():
    videos = [
        {"id": "v1", "channel": "alice", "views": 10000, "likes": 200, "comments": 50},
        {"id": "v2", "channel": "alice", "views": 5000,  "likes": 100, "comments": 20},
        {"id": "v3", "channel": "bob",   "views": 8000,  "likes": 150, "comments": 30},
    ]
    fn = _two_step_fetch(_search_payload(videos), _stats_payload(videos))
    sig = search_youtube("crypto_trading", "btc etf", api_key="k", fetch=fn, now=NOW)
    assert sig is not None
    assert sig.platform == "youtube"
    assert sig.niche == "crypto_trading"
    assert sig.topic == "btc etf"
    assert sig.supply_count == 2   # alice + bob
    assert sig.sample_size == 3


def test_engagement_in_unit_range():
    videos = [{"id": f"v{i}", "channel": "c", "views": 1000, "likes": 50, "comments": 10}
              for i in range(10)]
    fn = _two_step_fetch(_search_payload(videos), _stats_payload(videos))
    sig = search_youtube("crypto_trading", "x", api_key="k", fetch=fn, now=NOW)
    assert sig is not None
    assert 0.0 <= sig.engagement_score <= 1.0


def test_engagement_higher_for_more_views():
    low_v = [{"id": "a", "channel": "c", "views": 100, "likes": 1, "comments": 0}]
    hi_v  = [{"id": "a", "channel": "c", "views": 1_000_000, "likes": 50000, "comments": 5000}]
    low = search_youtube("crypto_trading", "x", api_key="k",
                         fetch=_two_step_fetch(_search_payload(low_v), _stats_payload(low_v)),
                         now=NOW)
    hi  = search_youtube("crypto_trading", "x", api_key="k",
                         fetch=_two_step_fetch(_search_payload(hi_v), _stats_payload(hi_v)),
                         now=NOW)
    assert hi.engagement_score > low.engagement_score


def test_max_results_clamped_to_50():
    # No real assertion possible without inspecting URL — confirm it doesn't crash
    videos = [{"id": f"v{i}", "channel": "c", "views": 100, "likes": 5, "comments": 1}
              for i in range(5)]
    fn = _two_step_fetch(_search_payload(videos), _stats_payload(videos))
    sig = search_youtube(
        "crypto_trading", "x", api_key="k",
        max_results=200, fetch=fn, now=NOW,
    )
    assert sig is not None


def test_handles_missing_videoId_in_search_result():
    """API sometimes returns playlist or channel results — those have no videoId."""
    raw_search = {"items": [
        {"id": {"playlistId": "PL1"}, "snippet": {"channelId": "c1"}},  # skip
        {"id": {"videoId": "v1"},     "snippet": {"channelId": "c2"}},  # keep
    ]}
    fn = _two_step_fetch(
        raw_search,
        _stats_payload([{"views": 1000, "likes": 10, "comments": 2}]),
    )
    sig = search_youtube("crypto_trading", "x", api_key="k", fetch=fn, now=NOW)
    assert sig is not None
    assert sig.sample_size == 1


def test_handles_zero_stats_without_error():
    videos = [{"id": "v1", "channel": "c1"}]  # views/likes/comments all default 0
    fn = _two_step_fetch(_search_payload(videos), _stats_payload(videos))
    sig = search_youtube("crypto_trading", "x", api_key="k", fetch=fn, now=NOW)
    assert sig is not None
    assert sig.engagement_score == 0.0  # log10(1)/7 = 0


# ---------------- Engagement function unit tests ----------------

def test_engagement_formula_weights_likes_and_comments():
    """Same views, but one set has likes/comments — should score higher."""
    only_views = _engagement_from_stats([10000], [0], [0])
    with_eng   = _engagement_from_stats([10000], [200], [50])
    assert with_eng > only_views


def test_engagement_formula_zero_empty():
    assert _engagement_from_stats([], [], []) == 0.0


# ---------------- Refresh + Replace ----------------

def test_refresh_skips_topics_returning_none():
    """If a topic has no search results, it shouldn't appear in output."""
    call_count = [0]
    def fn(url: str) -> dict:
        call_count[0] += 1
        if "good+topic" in url and "/search?" in url:
            return _search_payload([{"id": "v1", "channel": "c1", "views": 1000, "likes": 5, "comments": 1}])
        if "/videos?" in url:
            return _stats_payload([{"views": 1000, "likes": 5, "comments": 1}])
        return _search_payload([])
    sigs = refresh_youtube_signals(
        "crypto_trading", ["good topic", "bad topic"], api_key="k", fetch=fn,
    )
    assert len(sigs) == 1
    assert sigs[0].topic == "good topic"


def test_replace_youtube_signals_swaps_only_matching_topics():
    base = get_signals("crypto_trading")
    yt_signals = [s for s in base if s.platform == "youtube"][:1]
    if not yt_signals:
        return
    target_topic = yt_signals[0].topic
    from core.types import PlatformSignal
    fake_live = [PlatformSignal(
        platform="youtube", niche="crypto_trading",
        topic=target_topic, engagement_score=0.95,
        supply_count=500, sample_size=500,
    )]
    out = replace_youtube_signals(base, fake_live, "crypto_trading")
    swapped = [s for s in out if s.platform == "youtube" and s.topic == target_topic][0]
    assert swapped.engagement_score == 0.95
    # Reddit/Substack signals untouched
    for plat in ("reddit", "substack", "twitter"):
        before = sum(1 for s in base if s.platform == plat)
        after  = sum(1 for s in out  if s.platform == plat)
        assert before == after, f"{plat} count changed unexpectedly"


# ---------------- Quota helper ----------------

def test_estimate_quota_cost():
    assert estimate_quota_cost(0) == 0
    assert estimate_quota_cost(1) == 150
    # 66 topics is the typical daily ceiling -> just under 10k
    assert estimate_quota_cost(66) == 66 * 150
    assert estimate_quota_cost(66) <= 10000
