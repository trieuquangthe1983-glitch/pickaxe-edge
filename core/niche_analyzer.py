"""Niche analyzer: summarize platform-by-platform demand/supply for a niche."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .types import PLATFORMS, Platform, PlatformSignal


@dataclass(frozen=True)
class PlatformSummary:
    platform: Platform
    topic_count: int
    avg_engagement: float
    total_supply: int
    saturation: str   # "underserved" | "balanced" | "saturated"
    top_topics: tuple[str, ...]


@dataclass(frozen=True)
class NicheReport:
    niche: str
    summaries: tuple[PlatformSummary, ...]
    recommended_target_platforms: tuple[Platform, ...]
    recommended_source_platforms: tuple[Platform, ...]


def _classify_saturation(avg_supply_per_topic: float) -> str:
    if avg_supply_per_topic < 5:
        return "underserved"
    if avg_supply_per_topic < 20:
        return "balanced"
    return "saturated"


def analyze_niche(signals: Iterable[PlatformSignal], niche: str) -> NicheReport:
    """Build per-platform summary and recommend sources (high demand) and targets (low supply)."""
    relevant = [s for s in signals if s.niche == niche]
    summaries: list[PlatformSummary] = []

    for plat in PLATFORMS:
        plat_sigs = [s for s in relevant if s.platform == plat]
        if not plat_sigs:
            summaries.append(PlatformSummary(
                platform=plat,
                topic_count=0,
                avg_engagement=0.0,
                total_supply=0,
                saturation="underserved",
                top_topics=(),
            ))
            continue
        total_supply = sum(s.supply_count for s in plat_sigs)
        avg_eng = sum(s.engagement_score for s in plat_sigs) / len(plat_sigs)
        avg_supply = total_supply / len(plat_sigs)
        top = sorted(plat_sigs, key=lambda s: s.engagement_score, reverse=True)[:3]
        summaries.append(PlatformSummary(
            platform=plat,
            topic_count=len(plat_sigs),
            avg_engagement=round(avg_eng, 4),
            total_supply=total_supply,
            saturation=_classify_saturation(avg_supply),
            top_topics=tuple(s.topic for s in top),
        ))

    # Recommend SOURCE = high avg engagement (demand validated there)
    sources = sorted(
        (s for s in summaries if s.topic_count > 0),
        key=lambda s: s.avg_engagement,
        reverse=True,
    )[:3]
    # Recommend TARGET = underserved (low supply, room to enter)
    targets = sorted(
        (s for s in summaries if s.saturation in ("underserved", "balanced")),
        key=lambda s: s.total_supply,
    )[:3]

    return NicheReport(
        niche=niche,
        summaries=tuple(summaries),
        recommended_target_platforms=tuple(s.platform for s in targets),
        recommended_source_platforms=tuple(s.platform for s in sources),
    )
