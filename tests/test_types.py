"""Type invariants — defensive checks at the boundary."""

import pytest

from core.types import CreatorProfile, EdgeScore, PlatformSignal


def test_platform_signal_rejects_engagement_out_of_range():
    with pytest.raises(ValueError):
        PlatformSignal(platform="youtube", niche="x", topic="t",
                       engagement_score=1.5, supply_count=1)


def test_platform_signal_rejects_negative_supply():
    with pytest.raises(ValueError):
        PlatformSignal(platform="youtube", niche="x", topic="t",
                       engagement_score=0.5, supply_count=-1)


def test_creator_profile_rejects_mismatched_weights():
    with pytest.raises(ValueError):
        CreatorProfile(handle="@x", niche="n",
                       topics=("a", "b"), topic_weights=(0.5,),
                       vocabulary=frozenset())


def test_creator_profile_rejects_weights_not_summing_to_one():
    with pytest.raises(ValueError):
        CreatorProfile(handle="@x", niche="n",
                       topics=("a", "b"), topic_weights=(0.3, 0.3),
                       vocabulary=frozenset())


def test_edge_score_weights_sum_to_one():
    weights = EdgeScore.weights()
    assert abs(sum(weights.values()) - 1.0) < 1e-9
