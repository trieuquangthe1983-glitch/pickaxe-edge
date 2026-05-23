"""Domain types — small, immutable, testable."""

from dataclasses import dataclass, field
from typing import Literal

Platform = Literal["youtube", "tiktok", "twitter", "linkedin", "reddit", "substack"]

PLATFORMS: tuple[Platform, ...] = (
    "youtube", "tiktok", "twitter", "linkedin", "reddit", "substack"
)

Format = Literal["long_video", "short_video", "thread", "post", "discussion", "longform_text"]

NATIVE_FORMAT: dict[Platform, Format] = {
    "youtube": "long_video",
    "tiktok": "short_video",
    "twitter": "thread",
    "linkedin": "post",
    "reddit": "discussion",
    "substack": "longform_text",
}


@dataclass(frozen=True)
class PlatformSignal:
    """One data point: 'topic T on platform P has engagement E with supply S'."""
    platform: Platform
    niche: str
    topic: str
    engagement_score: float  # 0..1, demand proxy (views/likes/upvotes normalized)
    supply_count: int        # how many creators produced this in the last 30d
    sample_size: int = 1     # how many posts this signal aggregates

    def __post_init__(self) -> None:
        if not 0.0 <= self.engagement_score <= 1.0:
            raise ValueError(f"engagement_score out of range: {self.engagement_score}")
        if self.supply_count < 0:
            raise ValueError(f"supply_count negative: {self.supply_count}")


@dataclass(frozen=True)
class ArbitrageOpportunity:
    """A topic with proven demand on source platform but low supply on target."""
    topic: str
    source_platform: Platform
    target_platform: Platform
    demand_at_source: float   # 0..1
    supply_at_target: int
    score: float              # 0..1, higher = better
    difficulty: float         # 0..1, higher = harder to execute
    rationale: str

    @property
    def expected_value(self) -> float:
        """Heuristic EV proxy: score discounted by difficulty."""
        return self.score * (1.0 - 0.5 * self.difficulty)


@dataclass(frozen=True)
class CreatorProfile:
    """A creator's content fingerprint for edge scoring."""
    handle: str
    niche: str
    topics: tuple[str, ...]                # ordered by frequency
    topic_weights: tuple[float, ...]       # sum to 1.0
    vocabulary: frozenset[str]             # distinctive phrases they use
    audience_overlap: dict[str, float] = field(default_factory=dict)  # other creators' handle -> overlap
    avg_engagement: float = 0.0            # likes/views normalized 0..1
    comments_per_like: float = 0.0         # depth proxy
    hook_patterns: tuple[str, ...] = ()    # opening patterns of best posts

    def __post_init__(self) -> None:
        if len(self.topics) != len(self.topic_weights):
            raise ValueError("topics and topic_weights length mismatch")
        if self.topic_weights and abs(sum(self.topic_weights) - 1.0) > 1e-6:
            raise ValueError(f"topic_weights must sum to 1.0, got {sum(self.topic_weights)}")


@dataclass(frozen=True)
class EdgeScore:
    """Quantified differentiation. 0..1 each component, weighted overall."""
    vocabulary_uniqueness: float
    topic_concentration: float
    audience_cohesion: float
    engagement_depth: float
    hook_repeatability: float
    overall: float
    verdict: str  # human-readable diagnosis

    @staticmethod
    def weights() -> dict[str, float]:
        return {
            "vocabulary_uniqueness": 0.25,
            "topic_concentration": 0.20,
            "audience_cohesion": 0.15,
            "engagement_depth": 0.20,
            "hook_repeatability": 0.20,
        }
