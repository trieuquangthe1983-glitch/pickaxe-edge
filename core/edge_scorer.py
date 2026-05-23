"""Edge scorer: quantify a creator's actual differentiation.

Most creator analytics measure volume (followers, views). This measures EDGE —
whether you're standing out enough to justify continued investment in this niche.
"""

from __future__ import annotations

from collections import Counter
from typing import Iterable

from .types import CreatorProfile, EdgeScore


def _herfindahl(weights: Iterable[float]) -> float:
    """Concentration index 0..1. 1.0 = monopoly (one topic), low = scattered."""
    return sum(w * w for w in weights)


def _vocabulary_uniqueness(
    creator_vocab: frozenset[str],
    peer_vocabs: Iterable[frozenset[str]],
) -> float:
    """Fraction of creator vocabulary that doesn't appear in any peer's vocabulary."""
    if not creator_vocab:
        return 0.0
    peer_union: set[str] = set()
    for pv in peer_vocabs:
        peer_union |= pv
    unique = creator_vocab - peer_union
    return len(unique) / len(creator_vocab)


def _audience_cohesion(overlap: dict[str, float]) -> float:
    """Average pairwise overlap with top peers — high cohesion = tight tribe."""
    if not overlap:
        return 0.0
    values = list(overlap.values())
    return sum(values) / len(values)


def _engagement_depth(comments_per_like: float) -> float:
    """Map comments/likes ratio to 0..1. >0.10 is exceptional; 0.02 is typical."""
    if comments_per_like <= 0:
        return 0.0
    # Diminishing returns above 0.10
    return min(1.0, comments_per_like / 0.10)


def _hook_repeatability(hooks: tuple[str, ...]) -> float:
    """If best posts share opening patterns, that's a repeatable formula."""
    if not hooks:
        return 0.0
    counts = Counter(hooks)
    most_common_count = counts.most_common(1)[0][1]
    return most_common_count / len(hooks)


def _verdict(
    *,
    concentration: float,
    uniqueness: float,
    depth: float,
    cohesion: float,
    repeatability: float,
) -> str:
    """Plain-English diagnosis. Best-outcome verdicts evaluated first so they
    win over partial-match verdicts when a creator scores well on multiple axes.
    """
    # Strongest outcome first — real edge beats deep-audience-only when both hold
    if concentration >= 0.45 and uniqueness >= 0.35:
        return (
            "REAL EDGE - focused niche, distinctive voice. Double down. "
            "Risk: complacency. Stress-test by trying an adjacent niche."
        )
    if concentration < 0.25 and uniqueness < 0.25:
        return (
            "GENERALIST - you cover many topics and your vocabulary blends with peers. "
            "You will struggle to be referred. Pick ONE topic and develop a distinctive lexicon."
        )
    if concentration >= 0.45 and uniqueness < 0.20:
        return (
            "FOCUSED BUT INDISTINGUISHABLE - you're specialized but use the same language as competitors. "
            "Develop signature phrases, frameworks, or naming conventions."
        )
    if depth >= 0.60 and concentration >= 0.30:
        return (
            "DEEP AUDIENCE - high comment/like ratio means engaged tribe. "
            "Monetize via community/cohort, not ads."
        )
    if repeatability >= 0.60 and cohesion >= 0.40:
        return (
            "REPEATABLE FORMULA + TIGHT TRIBE - you have a system. "
            "Scale via volume of the same formula, not experiments."
        )
    return (
        "MIXED SIGNALS - no single component is broken but no clear edge either. "
        "Pick the weakest of vocabulary, concentration, depth and invest 90 days on it."
    )


def score_creator(
    profile: CreatorProfile,
    peer_profiles: Iterable[CreatorProfile],
) -> EdgeScore:
    """Compute edge score for a creator vs their peer set."""
    peer_vocabs = [p.vocabulary for p in peer_profiles if p.handle != profile.handle]

    uniqueness = _vocabulary_uniqueness(profile.vocabulary, peer_vocabs)
    concentration = _herfindahl(profile.topic_weights)
    cohesion = _audience_cohesion(profile.audience_overlap)
    depth = _engagement_depth(profile.comments_per_like)
    repeatability = _hook_repeatability(profile.hook_patterns)

    weights = EdgeScore.weights()
    overall = round(
        uniqueness * weights["vocabulary_uniqueness"]
        + concentration * weights["topic_concentration"]
        + cohesion * weights["audience_cohesion"]
        + depth * weights["engagement_depth"]
        + repeatability * weights["hook_repeatability"],
        4,
    )

    verdict = _verdict(
        concentration=concentration,
        uniqueness=uniqueness,
        depth=depth,
        cohesion=cohesion,
        repeatability=repeatability,
    )

    return EdgeScore(
        vocabulary_uniqueness=round(uniqueness, 4),
        topic_concentration=round(concentration, 4),
        audience_cohesion=round(cohesion, 4),
        engagement_depth=round(depth, 4),
        hook_repeatability=round(repeatability, 4),
        overall=overall,
        verdict=verdict,
    )
