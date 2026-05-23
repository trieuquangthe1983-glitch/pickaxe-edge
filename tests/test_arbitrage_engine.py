"""Arbitrage engine: deterministic behaviour on hand-built and seed data."""

from core.arbitrage_engine import (
    find_opportunities,
    format_difficulty,
    opportunities_by_target,
)
from core.types import NATIVE_FORMAT, PlatformSignal
from data.sources import get_signals


def test_format_difficulty_self_is_trivial():
    assert format_difficulty("long_video", "long_video") < 0.1


def test_format_difficulty_thread_to_post_is_low():
    # Thread -> LinkedIn post is the easiest real cross-format move
    assert format_difficulty("thread", "post") < 0.25


def test_format_difficulty_short_video_to_longform_is_high():
    assert format_difficulty("short_video", "longform_text") > 0.6


def test_find_opportunities_returns_empty_for_unknown_niche():
    sigs = get_signals("crypto_trading")
    assert find_opportunities(sigs, niche="does_not_exist") == []


def test_find_opportunities_returns_empty_below_floor():
    # Single low-demand signal — nothing to mine
    sigs = [PlatformSignal(platform="youtube", niche="n",
                           topic="t", engagement_score=0.1, supply_count=0)]
    assert find_opportunities(sigs, niche="n") == []


def test_find_opportunities_detects_handcrafted_arbitrage():
    # Two platforms with signals; engine should consider missing-signal platforms
    # as 0-supply candidates too, so we provide a saturated platform set.
    sigs = [
        PlatformSignal(platform="twitter", niche="n", topic="alpha",
                       engagement_score=0.90, supply_count=20, sample_size=500),
        PlatformSignal(platform="tiktok",  niche="n", topic="alpha",
                       engagement_score=0.10, supply_count=0,  sample_size=2),
        # Saturate all other platforms so the only viable target is tiktok
        PlatformSignal(platform="youtube",  niche="n", topic="alpha",
                       engagement_score=0.5, supply_count=40),
        PlatformSignal(platform="linkedin", niche="n", topic="alpha",
                       engagement_score=0.5, supply_count=40),
        PlatformSignal(platform="reddit",   niche="n", topic="alpha",
                       engagement_score=0.5, supply_count=40),
        PlatformSignal(platform="substack", niche="n", topic="alpha",
                       engagement_score=0.5, supply_count=40),
    ]
    opps = find_opportunities(sigs, niche="n")
    assert opps, "Expected at least one opportunity"
    top = opps[0]
    assert top.topic == "alpha"
    # Twitter is the demand source, tiktok the only valid (low-supply) target
    assert top.source_platform == "twitter"
    assert top.target_platform == "tiktok"
    assert top.demand_at_source == 0.90
    assert top.supply_at_target == 0


def test_find_opportunities_respects_supply_ceiling():
    # Target has too many creators -> not an arbitrage
    sigs = [
        PlatformSignal(platform="twitter", niche="n", topic="t",
                       engagement_score=0.9, supply_count=20),
        PlatformSignal(platform="tiktok",  niche="n", topic="t",
                       engagement_score=0.5, supply_count=50),
    ]
    opps = find_opportunities(sigs, niche="n", supply_ceiling=8)
    assert all(o.target_platform != "tiktok" for o in opps), \
        "Saturated target must be excluded"


def test_find_opportunities_ranks_by_expected_value():
    sigs = get_signals("crypto_trading")
    opps = find_opportunities(sigs, niche="crypto_trading", max_results=10)
    assert len(opps) > 0
    evs = [o.expected_value for o in opps]
    assert evs == sorted(evs, reverse=True), "Opportunities must be sorted by EV desc"


def test_opportunities_by_target_groups_correctly():
    sigs = get_signals("indie_saas")
    opps = find_opportunities(sigs, niche="indie_saas", max_results=20)
    grouped = opportunities_by_target(opps)
    for plat, lst in grouped.items():
        assert all(o.target_platform == plat for o in lst)
        # within-group sorted
        evs = [o.expected_value for o in lst]
        assert evs == sorted(evs, reverse=True)


def test_seeded_crypto_arbitrage_finds_perp_basis_decay():
    """Sanity: the seed deliberately has 'perp basis decay 101' as a substack→linkedin/tiktok gap."""
    sigs = get_signals("crypto_trading")
    opps = find_opportunities(sigs, niche="crypto_trading", max_results=20)
    topics_found = {o.topic for o in opps}
    assert "perp basis decay 101" in topics_found


def test_seeded_seed_signals_have_no_self_arbitrage():
    """A topic should never be arbitraged from a platform to itself."""
    sigs = get_signals()
    for niche in {s.niche for s in sigs}:
        for o in find_opportunities(sigs, niche=niche, max_results=50):
            assert o.source_platform != o.target_platform


def test_native_format_covers_all_platforms():
    from core.types import PLATFORMS
    for plat in PLATFORMS:
        assert plat in NATIVE_FORMAT
