"""YouTube Data API v3 — source #3, REAL engagement.

Why this is the strongest source after Reddit:
- Public quota of 10k units/day (free), no payment required
- Returns view/like/comment counts -> real engagement, not a proxy
- Search by topic + publishedAfter window maps cleanly to our model

Quota cost per topic search:
- 1 search call            = 100 units
- 1 batched videos.list    =   1 unit per video, capped at 50 = 50 units
- Total per topic          = ~150 units
- 10k/day free quota       = ~66 topic searches/day
- A full 6-niche x ~4 topic scan = ~24 searches = fits 2-3 scans/day

Get an API key (5 minutes):
1. https://console.cloud.google.com -> create project (or reuse one)
2. APIs & Services -> Library -> "YouTube Data API v3" -> Enable
3. APIs & Services -> Credentials -> Create Credentials -> API Key
4. Restrict to "YouTube Data API v3" for safety
5. Pass to search_youtube() or set env YOUTUBE_API_KEY
"""

from __future__ import annotations

import json
import math
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from typing import Callable, Iterable

from core.types import PlatformSignal

USER_AGENT = "pickaxe-edge/0.1 (research tool)"
SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"
VIDEOS_URL = "https://www.googleapis.com/youtube/v3/videos"

FetchJsonFn = Callable[[str], dict]


def _default_fetch(url: str) -> dict:
    """Real network fetch — tests inject a fake."""
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.load(resp)


def _engagement_from_stats(
    views: list[int],
    likes: list[int],
    comments: list[int],
) -> float:
    """Map per-video stats to 0..1.

    Weighted sum across all videos: views + 50*likes + 100*comments. Likes
    and comments require active engagement so they're amplified vs passive
    view counts. log10 then divided by 7 so:
    - 10k weighted total -> 0.57
    - 100k                -> 0.71
    - 1M                  -> 0.86
    - 10M                 -> clipped 1.0
    """
    if not views:
        return 0.0
    weighted_total = sum(
        max(0, v) + 50 * max(0, l) + 100 * max(0, c)
        for v, l, c in zip(views, likes, comments)
    )
    return max(0.0, min(1.0, math.log10(weighted_total + 1) / 7.0))


def search_youtube(
    niche: str,
    topic: str,
    *,
    api_key: str,
    days_window: int = 30,
    max_results: int = 25,
    fetch: FetchJsonFn = _default_fetch,
    now: datetime | None = None,
) -> PlatformSignal | None:
    """Search YouTube for videos matching topic in the window.

    Returns aggregated PlatformSignal or None if no key / no results / API error.
    """
    if not api_key:
        return None
    if max_results > 50:
        max_results = 50  # API hard limit per call

    if now is None:
        now = datetime.now(timezone.utc)
    published_after = (now - timedelta(days=days_window)).strftime("%Y-%m-%dT%H:%M:%SZ")

    search_qs = urllib.parse.urlencode({
        "part": "snippet",
        "q": topic,
        "type": "video",
        "order": "viewCount",
        "publishedAfter": published_after,
        "maxResults": str(max_results),
        "key": api_key,
    })
    try:
        search_result = fetch(f"{SEARCH_URL}?{search_qs}")
    except Exception:
        return None

    items = search_result.get("items", []) or []
    video_ids: list[str] = []
    channels: set[str] = set()
    for it in items:
        vid_id = (it.get("id") or {}).get("videoId")
        chan_id = (it.get("snippet") or {}).get("channelId")
        if vid_id:
            video_ids.append(vid_id)
        if chan_id:
            channels.add(chan_id)

    if not video_ids:
        return None

    stats_qs = urllib.parse.urlencode({
        "part": "statistics",
        "id": ",".join(video_ids),
        "key": api_key,
    })
    try:
        stats_result = fetch(f"{VIDEOS_URL}?{stats_qs}")
    except Exception:
        return None

    views: list[int] = []
    likes: list[int] = []
    comments: list[int] = []
    for v in stats_result.get("items", []) or []:
        s = v.get("statistics", {}) or {}
        views.append(int(s.get("viewCount") or 0))
        likes.append(int(s.get("likeCount") or 0))
        comments.append(int(s.get("commentCount") or 0))

    if not views:
        return None

    return PlatformSignal(
        platform="youtube",
        niche=niche,
        topic=topic,
        engagement_score=round(_engagement_from_stats(views, likes, comments), 4),
        supply_count=len(channels),
        sample_size=len(views),
    )


def refresh_youtube_signals(
    niche: str,
    topics: Iterable[str],
    *,
    api_key: str,
    days_window: int = 30,
    max_results: int = 25,
    fetch: FetchJsonFn = _default_fetch,
) -> list[PlatformSignal]:
    """Fetch live YouTube signals for a list of topics in a niche."""
    out: list[PlatformSignal] = []
    for topic in topics:
        sig = search_youtube(
            niche, topic,
            api_key=api_key,
            days_window=days_window,
            max_results=max_results,
            fetch=fetch,
        )
        if sig is not None:
            out.append(sig)
    return out


def replace_youtube_signals(
    base_signals: list[PlatformSignal],
    live_signals: list[PlatformSignal],
    niche: str,
) -> list[PlatformSignal]:
    """Swap mock YouTube signals for live ones on matching topics."""
    live_by_topic = {s.topic: s for s in live_signals if s.platform == "youtube"}
    out: list[PlatformSignal] = []
    for s in base_signals:
        if s.platform == "youtube" and s.niche == niche and s.topic in live_by_topic:
            out.append(live_by_topic[s.topic])
        else:
            out.append(s)
    return out


def estimate_quota_cost(num_topics: int) -> int:
    """Predict total YouTube quota consumed for N topic searches."""
    # 100 (search) + 1 (videos stats — batched, counts as ~1 regardless of N)
    # Conservative: assume 1 unit per video, max 50 per topic
    return num_topics * (100 + 50)
