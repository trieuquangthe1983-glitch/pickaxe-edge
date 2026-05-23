"""Edge scorer: ordering matters more than absolute numbers."""

from core.edge_scorer import score_creator
from data.creator_seeds import SAMPLE_CREATORS, peer_set


def test_generic_creator_scores_lower_than_focused_creator():
    crypto_peers = peer_set("crypto_trading")
    generic = score_creator(SAMPLE_CREATORS["@generic_crypto_guy"], crypto_peers)
    focused = score_creator(SAMPLE_CREATORS["@basis_trader"], crypto_peers)
    assert focused.overall > generic.overall, (
        f"Focused creator must score higher: focused={focused.overall} "
        f"generic={generic.overall}"
    )


def test_focused_creator_gets_real_edge_verdict():
    peers = peer_set("crypto_trading")
    s = score_creator(SAMPLE_CREATORS["@basis_trader"], peers)
    assert "REAL EDGE" in s.verdict


def test_generalist_gets_generalist_verdict():
    peers = peer_set("crypto_trading")
    s = score_creator(SAMPLE_CREATORS["@generic_crypto_guy"], peers)
    assert "GENERALIST" in s.verdict


def test_focused_but_indistinguishable_caught():
    peers = peer_set("longevity")
    s = score_creator(SAMPLE_CREATORS["@another_zone2_guy"], peers)
    # Concentration is high (0.5^2 + 0.25^2 + 0.15^2 + 0.10^2 = 0.345)
    # but vocabulary mostly overlaps with peers
    assert s.topic_concentration >= 0.30
    assert s.vocabulary_uniqueness < 0.30


def test_all_components_in_unit_range():
    peers = peer_set("crypto_trading")
    s = score_creator(SAMPLE_CREATORS["@basis_trader"], peers)
    for v in (s.vocabulary_uniqueness, s.topic_concentration, s.audience_cohesion,
              s.engagement_depth, s.hook_repeatability, s.overall):
        assert 0.0 <= v <= 1.0


def test_empty_peer_set_gives_full_uniqueness():
    s = score_creator(SAMPLE_CREATORS["@basis_trader"], [])
    assert s.vocabulary_uniqueness == 1.0
