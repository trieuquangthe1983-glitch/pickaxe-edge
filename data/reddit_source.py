"""Reddit live data source — first real platform integration.

Reddit's public JSON endpoints work without auth (with a User-Agent), and
search is per-subreddit, which maps cleanly to our niche concept.

Design notes:
- A `fetch` callable is injected so tests can mock the network.
- Engagement is normalized via log10(score + 2*comments) to dampen
  the long-tail of viral posts.
- supply_count = unique non-bot authors among results (proxy for "creators
  competing on this topic in the last <window>").
"""

from __future__ import annotations

import json
import math
import urllib.parse
import urllib.request
from typing import Callable, Iterable

from core.types import PlatformSignal


USER_AGENT = "pickaxe-edge/0.1 (research tool)"

NICHE_SUBREDDITS: dict[str, list[str]] = {
    "crypto_trading":   ["CryptoCurrency", "CryptoMarkets", "Bitcoin"],
    "home_automation":  ["homeassistant", "smarthome"],
    "indie_saas":       ["SaaS", "Entrepreneur", "indiehackers"],
    "longevity":        ["longevity", "Biohackers"],
    "ai_engineering":   ["LocalLLaMA", "MachineLearning"],
    "personal_finance": ["personalfinance", "Bogleheads"],
}

BOT_AUTHORS = frozenset({"[deleted]", "AutoModerator", "[removed]"})


FetchFn = Callable[[str], dict]


def _default_fetch(url: str) -> dict:
    """Real network fetch. Tests inject a fake fetch instead."""
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=10) as resp:
        return json.load(resp)


def _normalize_engagement(scores: list[int], comments: list[int]) -> float:
    """Map (score, comments) per post to a 0..1 engagement proxy.

    Use the median weighted score to avoid one viral post dominating.
    log10(1000) -> 1.0; log10(1) -> 0; clipped.
    """
    if not scores:
        return 0.0
    weighted = [max(0, s) + 2 * max(0, c) for s, c in zip(scores, comments)]
    weighted.sort()
    median_weighted = weighted[len(weighted) // 2]
    return max(0.0, min(1.0, math.log10(median_weighted + 1) / 3.0))


def search_reddit(
    niche: str,
    topic: str,
    *,
    time_filter: str = "month",
    per_sub_limit: int = 25,
    fetch: FetchFn = _default_fetch,
) -> PlatformSignal | None:
    """Search Reddit for posts matching topic across the niche's subreddits.

    Returns an aggregated PlatformSignal, or None if no results / niche unknown.
    """
    subs = NICHE_SUBREDDITS.get(niche, [])
    if not subs:
        return None

    q = urllib.parse.quote_plus(topic)
    scores: list[int] = []
    comments: list[int] = []
    creators: set[str] = set()

    for sub in subs:
        url = (
            f"https://www.reddit.com/r/{sub}/search.json"
            f"?q={q}&restrict_sr=1&sort=top&t={time_filter}&limit={per_sub_limit}"
        )
        try:
            data = fetch(url)
        except Exception:
            # Network/JSON errors per-sub are non-fatal — keep aggregating others
            continue
        for child in data.get("data", {}).get("children", []):
            d = child.get("data", {}) or {}
            scores.append(int(d.get("score") or 0))
            comments.append(int(d.get("num_comments") or 0))
            author = d.get("author")
            if author and author not in BOT_AUTHORS:
                creators.add(author)

    if not scores:
        return None

    return PlatformSignal(
        platform="reddit",
        niche=niche,
        topic=topic,
        engagement_score=round(_normalize_engagement(scores, comments), 4),
        supply_count=len(creators),
        sample_size=len(scores),
    )


def refresh_reddit_signals(
    niche: str,
    topics: Iterable[str],
    *,
    fetch: FetchFn = _default_fetch,
    time_filter: str = "month",
) -> list[PlatformSignal]:
    """Fetch live Reddit signals for a list of topics in a niche."""
    out: list[PlatformSignal] = []
    for topic in topics:
        sig = search_reddit(niche, topic, fetch=fetch, time_filter=time_filter)
        if sig is not None:
            out.append(sig)
    return out


def replace_reddit_signals(
    base_signals: list[PlatformSignal],
    live_signals: list[PlatformSignal],
    niche: str,
) -> list[PlatformSignal]:
    """Swap mock Reddit signals for live Reddit signals on matching topics.

    Non-Reddit signals and unmatched mock-Reddit signals are kept as-is.
    """
    live_by_topic = {s.topic: s for s in live_signals if s.platform == "reddit"}
    out: list[PlatformSignal] = []
    for s in base_signals:
        if s.platform == "reddit" and s.niche == niche and s.topic in live_by_topic:
            out.append(live_by_topic[s.topic])
        else:
            out.append(s)
    return out
