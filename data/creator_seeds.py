"""Sample creator profiles for edge audit demos."""

from __future__ import annotations

from core.types import CreatorProfile

SAMPLE_CREATORS: dict[str, CreatorProfile] = {
    # Generalist — no edge
    "@generic_crypto_guy": CreatorProfile(
        handle="@generic_crypto_guy",
        niche="crypto_trading",
        topics=("btc", "eth", "altcoins", "memes", "macro", "trading"),
        topic_weights=(0.18, 0.17, 0.17, 0.16, 0.16, 0.16),
        vocabulary=frozenset({"moon", "wagmi", "lfg", "alpha", "bullish", "bearish", "dyor", "ngmi"}),
        audience_overlap={"@cryptoboi": 0.85, "@moonboy": 0.82, "@bullposter": 0.79},
        avg_engagement=0.32,
        comments_per_like=0.018,
        hook_patterns=("THIS is going to", "Wait until you see", "Bullish on", "Why X matters"),
    ),

    # Real edge — focused + distinctive vocabulary
    "@basis_trader": CreatorProfile(
        handle="@basis_trader",
        niche="crypto_trading",
        topics=("funding rates", "perp basis", "delta neutral", "carry trades", "vol surface"),
        topic_weights=(0.65, 0.20, 0.08, 0.05, 0.02),
        vocabulary=frozenset({
            "basis decay", "carry harvest", "settlement skew",
            "annualized perp yield", "convergence pin", "term structure roll",
        }),
        audience_overlap={"@quantgirl": 0.55, "@trad_desk": 0.48},
        avg_engagement=0.71,
        comments_per_like=0.082,
        hook_patterns=(
            "The basis curve is telling us",
            "The basis curve is telling us",
            "The basis curve is telling us",
            "Settlement-skew watch:",
            "Settlement-skew watch:",
        ),
    ),

    # Focused but indistinguishable — same words as peers
    "@another_zone2_guy": CreatorProfile(
        handle="@another_zone2_guy",
        niche="longevity",
        topics=("zone 2", "vo2max", "rapamycin", "cgm"),
        topic_weights=(0.50, 0.25, 0.15, 0.10),
        vocabulary=frozenset({"zone 2", "vo2max", "longevity", "rapamycin", "cgm", "mitochondria"}),
        audience_overlap={"@peter_attia_fan": 0.78, "@huberman_clip": 0.74},
        avg_engagement=0.45,
        comments_per_like=0.022,
        hook_patterns=("Zone 2 is", "VO2max matters because", "Most people get zone 2 wrong"),
    ),
}


def peer_set(niche: str) -> list[CreatorProfile]:
    """Synthetic peer baseline for a niche, used in uniqueness comparison."""
    if niche == "crypto_trading":
        return [
            CreatorProfile(
                handle="@cryptoboi", niche=niche,
                topics=("btc", "eth"), topic_weights=(0.6, 0.4),
                vocabulary=frozenset({"moon", "wagmi", "lfg", "alpha", "bullish", "bearish", "dyor"}),
            ),
            CreatorProfile(
                handle="@moonboy", niche=niche,
                topics=("memes", "alts"), topic_weights=(0.5, 0.5),
                vocabulary=frozenset({"moon", "wagmi", "lfg", "ngmi", "bullish"}),
            ),
            CreatorProfile(
                handle="@bullposter", niche=niche,
                topics=("macro", "btc"), topic_weights=(0.5, 0.5),
                vocabulary=frozenset({"alpha", "bullish", "bearish", "macro", "fed"}),
            ),
        ]
    if niche == "longevity":
        return [
            CreatorProfile(
                handle="@peter_attia_fan", niche=niche,
                topics=("zone 2", "vo2max"), topic_weights=(0.6, 0.4),
                vocabulary=frozenset({"zone 2", "vo2max", "longevity", "mitochondria", "lactate"}),
            ),
            CreatorProfile(
                handle="@huberman_clip", niche=niche,
                topics=("sleep", "rapamycin"), topic_weights=(0.5, 0.5),
                vocabulary=frozenset({"rapamycin", "cgm", "sleep", "circadian", "longevity"}),
            ),
        ]
    return []
