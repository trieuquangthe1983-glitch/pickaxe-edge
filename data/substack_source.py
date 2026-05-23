"""Substack RSS data source — source #2.

Substack publishes a standard RSS feed at `<pub>.substack.com/feed` for every
publication. No auth, no rate limit (within reason), no TOS issues.

Honest limitation: RSS does NOT expose engagement (likes/comments). So our
`engagement_score` here is a *demand proxy* derived from publication activity:
how many publications in the niche posted about the topic in the window.
If multiple respected publications are writing about it, demand is implied.

This is structurally different from Reddit (which has real engagement metrics).
The arbitrage engine treats both as comparable 0..1 signals -- be aware of
this when interpreting Substack-sourced opportunities.

Architecture:
- Curated per-niche publications + user-override parameter
- Stdlib XML parsing (no extra deps)
- Time-window filtering via RFC 822 pubDate
- Keyword match against title + description
"""

from __future__ import annotations

import math
import re
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
from typing import Callable, Iterable

from core.types import PlatformSignal

USER_AGENT = "pickaxe-edge/0.1 (research tool)"

# Curated defaults. These slugs are well-known but verify before scaling outreach
# (publications move platforms / change names). Users SHOULD override via the
# `publications` parameter once they know the real names in their niche.
NICHE_PUBLICATIONS: dict[str, list[str]] = {
    "crypto_trading":   ["cryptohayes", "pomp", "bankless"],
    "home_automation":  ["thehookup"],  # niche is sparse on Substack
    "indie_saas":       ["lennysnewsletter", "tomtunguz", "growthunhinged"],
    "longevity":        ["thedrive"],   # uncertain — override recommended
    "ai_engineering":   ["interconnected", "every"],
    "personal_finance": ["abnormalreturns", "ofdollarsanddata"],
}

RSS_NS = {"dc": "http://purl.org/dc/elements/1.1/"}


FetchTextFn = Callable[[str], str]


def _default_fetch(url: str) -> str:
    """Real network fetch — tests inject a fake."""
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=10) as resp:
        raw = resp.read()
    return raw.decode("utf-8", errors="replace")


def _pub_to_feed_url(pub: str) -> str:
    """Accept either a slug ('pomp') or a full feed URL."""
    if pub.startswith(("http://", "https://")):
        return pub
    return f"https://{pub}.substack.com/feed"


def _parse_pubdate(s: str | None) -> datetime | None:
    if not s:
        return None
    try:
        dt = parsedate_to_datetime(s)
    except (TypeError, ValueError):
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt


def _strip_html(s: str) -> str:
    """Cheap HTML strip for matching — RSS descriptions often have <p> tags."""
    return re.sub(r"<[^>]+>", " ", s)


def _parse_rss(xml_text: str) -> list[dict]:
    """Parse Substack RSS into a list of post dicts. Returns [] on malformed XML."""
    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError:
        return []
    channel = root.find("channel")
    if channel is None:
        return []

    posts: list[dict] = []
    for item in channel.findall("item"):
        d: dict = {}
        for tag in ("title", "link", "description", "pubDate"):
            el = item.find(tag)
            if el is not None and el.text:
                d[tag] = el.text.strip()
        creator = item.find("dc:creator", RSS_NS)
        if creator is not None and creator.text:
            d["author"] = creator.text.strip()
        posts.append(d)
    return posts


def _extract_keywords(topic: str) -> list[str]:
    """Tokenize topic into matchable keywords (>= 3 chars, lowercase)."""
    return [w.lower() for w in re.findall(r"\w+", topic) if len(w) >= 3]


def _post_matches(post: dict, keywords: list[str]) -> bool:
    if not keywords:
        return False
    haystack = (
        post.get("title", "") + " " + _strip_html(post.get("description", ""))
    ).lower()
    # All keywords must appear (AND semantics) — keeps matches relevant
    return all(k in haystack for k in keywords)


def search_substack(
    niche: str,
    topic: str,
    *,
    publications: list[str] | None = None,
    days_window: int = 30,
    fetch: FetchTextFn = _default_fetch,
    now: datetime | None = None,
) -> PlatformSignal | None:
    """Search Substack publications for posts matching `topic` in the window.

    Returns an aggregated PlatformSignal or None if no matches / no publications.
    """
    pubs = publications if publications is not None else NICHE_PUBLICATIONS.get(niche, [])
    if not pubs:
        return None

    keywords = _extract_keywords(topic)
    if not keywords:
        return None

    if now is None:
        now = datetime.now(timezone.utc)
    cutoff = now - timedelta(days=days_window)

    matches: list[dict] = []
    creators: set[str] = set()

    for pub in pubs:
        url = _pub_to_feed_url(pub)
        try:
            xml = fetch(url)
        except Exception:
            # Per-pub failure non-fatal — keep aggregating others
            continue
        for post in _parse_rss(xml):
            pub_dt = _parse_pubdate(post.get("pubDate"))
            if pub_dt is not None and pub_dt < cutoff:
                continue
            if not _post_matches(post, keywords):
                continue
            matches.append(post)
            author = post.get("author") or pub
            creators.add(author)

    if not matches:
        return None

    # Engagement proxy: log10(matches + 1) / 1.5, clipped to 1.0
    # 10 matches -> 0.69; 30 matches -> 0.99
    engagement = max(0.0, min(1.0, math.log10(len(matches) + 1) / 1.5))

    return PlatformSignal(
        platform="substack",
        niche=niche,
        topic=topic,
        engagement_score=round(engagement, 4),
        supply_count=len(creators),
        sample_size=len(matches),
    )


def refresh_substack_signals(
    niche: str,
    topics: Iterable[str],
    *,
    publications: list[str] | None = None,
    fetch: FetchTextFn = _default_fetch,
    days_window: int = 30,
) -> list[PlatformSignal]:
    """Fetch live Substack signals for a list of topics in a niche."""
    out: list[PlatformSignal] = []
    for topic in topics:
        sig = search_substack(
            niche, topic,
            publications=publications,
            fetch=fetch,
            days_window=days_window,
        )
        if sig is not None:
            out.append(sig)
    return out


def replace_substack_signals(
    base_signals: list[PlatformSignal],
    live_signals: list[PlatformSignal],
    niche: str,
) -> list[PlatformSignal]:
    """Swap mock Substack signals for live ones on matching topics."""
    live_by_topic = {s.topic: s for s in live_signals if s.platform == "substack"}
    out: list[PlatformSignal] = []
    for s in base_signals:
        if s.platform == "substack" and s.niche == niche and s.topic in live_by_topic:
            out.append(live_by_topic[s.topic])
        else:
            out.append(s)
    return out
