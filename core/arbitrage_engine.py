"""Arbitrage engine: cross-platform white-space detection.

Core insight: if a topic has demand_score >= DEMAND_FLOOR on source platform
AND supply_count <= SUPPLY_CEILING on target platform, that's a white-space
opportunity — proven demand, low competition.
"""

from __future__ import annotations

from collections import defaultdict
from typing import Iterable

from .types import (
    NATIVE_FORMAT,
    PLATFORMS,
    ArbitrageOpportunity,
    Format,
    Platform,
    PlatformSignal,
)

DEMAND_FLOOR = 0.55       # source platform must show this level of engagement
SUPPLY_CEILING = 8        # target platform must have at most this many creators
MAX_SUPPLY_NORM = 50      # normalize supply for scoring


# Format adaptation difficulty: 0 = trivial, 1 = total rewrite.
# Asymmetric on purpose — e.g. long_video → short_video is easier than reverse.
_FORMAT_DIFFICULTY: dict[tuple[Format, Format], float] = {
    ("long_video", "short_video"): 0.25,
    ("long_video", "thread"): 0.35,
    ("long_video", "post"): 0.30,
    ("long_video", "discussion"): 0.50,
    ("long_video", "longform_text"): 0.45,

    ("short_video", "long_video"): 0.75,
    ("short_video", "thread"): 0.30,
    ("short_video", "post"): 0.25,
    ("short_video", "discussion"): 0.55,
    ("short_video", "longform_text"): 0.70,

    ("thread", "long_video"): 0.65,
    ("thread", "short_video"): 0.35,
    ("thread", "post"): 0.15,
    ("thread", "discussion"): 0.40,
    ("thread", "longform_text"): 0.30,

    ("post", "long_video"): 0.70,
    ("post", "short_video"): 0.40,
    ("post", "thread"): 0.20,
    ("post", "discussion"): 0.50,
    ("post", "longform_text"): 0.45,

    ("discussion", "long_video"): 0.55,
    ("discussion", "short_video"): 0.50,
    ("discussion", "thread"): 0.30,
    ("discussion", "post"): 0.35,
    ("discussion", "longform_text"): 0.25,

    ("longform_text", "long_video"): 0.60,
    ("longform_text", "short_video"): 0.70,
    ("longform_text", "thread"): 0.20,
    ("longform_text", "post"): 0.30,
    ("longform_text", "discussion"): 0.40,
}


def format_difficulty(src: Format, tgt: Format) -> float:
    if src == tgt:
        return 0.05
    return _FORMAT_DIFFICULTY.get((src, tgt), 0.5)


def _supply_penalty(supply: int) -> float:
    """Map supply count to a 0..1 penalty. 0 supply → 1.0, MAX_SUPPLY_NORM+ → 0."""
    if supply <= 0:
        return 1.0
    if supply >= MAX_SUPPLY_NORM:
        return 0.0
    return 1.0 - (supply / MAX_SUPPLY_NORM)


def _index_signals(signals: Iterable[PlatformSignal]) -> dict[tuple[str, Platform], PlatformSignal]:
    idx: dict[tuple[str, Platform], PlatformSignal] = {}
    for s in signals:
        key = (s.topic, s.platform)
        prior = idx.get(key)
        # Keep the signal with larger sample_size for stability
        if prior is None or s.sample_size > prior.sample_size:
            idx[key] = s
    return idx


def find_opportunities(
    signals: Iterable[PlatformSignal],
    niche: str,
    *,
    demand_floor: float = DEMAND_FLOOR,
    supply_ceiling: int = SUPPLY_CEILING,
    max_results: int = 20,
) -> list[ArbitrageOpportunity]:
    """Find arbitrage opportunities within a niche.

    For every (topic, source) with demand >= floor, check every other platform
    where supply <= ceiling and score the white-space gap.
    """
    relevant = [s for s in signals if s.niche == niche]
    if not relevant:
        return []

    idx = _index_signals(relevant)
    topics = sorted({s.topic for s in relevant})

    opps: list[ArbitrageOpportunity] = []
    for topic in topics:
        for src in PLATFORMS:
            src_sig = idx.get((topic, src))
            if src_sig is None or src_sig.engagement_score < demand_floor:
                continue
            for tgt in PLATFORMS:
                if tgt == src:
                    continue
                tgt_sig = idx.get((topic, tgt))
                tgt_supply = tgt_sig.supply_count if tgt_sig else 0
                if tgt_supply > supply_ceiling:
                    continue
                difficulty = format_difficulty(NATIVE_FORMAT[src], NATIVE_FORMAT[tgt])
                supply_score = _supply_penalty(tgt_supply)
                # Score = demand × supply-gap × (1 - difficulty/2)
                # difficulty is discounted in score and again in expected_value
                raw = src_sig.engagement_score * supply_score * (1.0 - 0.5 * difficulty)
                score = round(min(1.0, max(0.0, raw)), 4)
                rationale = (
                    f"'{topic}' has {src_sig.engagement_score:.2f} engagement on {src} "
                    f"(sample={src_sig.sample_size}) but only {tgt_supply} creators on {tgt}. "
                    f"Format shift {NATIVE_FORMAT[src]} -> {NATIVE_FORMAT[tgt]} is "
                    f"{'low' if difficulty < 0.3 else 'medium' if difficulty < 0.55 else 'high'} difficulty."
                )
                opps.append(ArbitrageOpportunity(
                    topic=topic,
                    source_platform=src,
                    target_platform=tgt,
                    demand_at_source=round(src_sig.engagement_score, 4),
                    supply_at_target=tgt_supply,
                    score=score,
                    difficulty=round(difficulty, 4),
                    rationale=rationale,
                ))

    opps.sort(key=lambda o: o.expected_value, reverse=True)
    return opps[:max_results]


def opportunities_by_target(
    opps: Iterable[ArbitrageOpportunity],
) -> dict[Platform, list[ArbitrageOpportunity]]:
    """Group opportunities by target platform — useful for 'which platform should I expand to'."""
    out: dict[Platform, list[ArbitrageOpportunity]] = defaultdict(list)
    for o in opps:
        out[o.target_platform].append(o)
    for plat in out:
        out[plat].sort(key=lambda o: o.expected_value, reverse=True)
    return dict(out)
