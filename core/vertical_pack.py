"""Vertical pack generator — niche-specific $99 productized info product.

A pack has two layers:
- EVERGREEN: curated content per niche (hooks, format adaptations, topic
  taxonomy, edge audit). Timeless, authored by domain expert.
- CURRENT: live arbitrage opportunities + 3 deep-dive execution plans.
  Stamped with `valid_through` date — creates a reason to buy quarterly refresh.

The same generator works across niches. Adding a new vertical pack is a content
swap (`data/<niche>_pack.py`), not a code change.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import Iterable

from .types import (
    NATIVE_FORMAT,
    PLATFORMS,
    ArbitrageOpportunity,
    Format,
    Platform,
    PlatformSignal,
)
from .arbitrage_engine import find_opportunities


@dataclass(frozen=True)
class DeepDive:
    """Execution plan for one arbitrage opportunity."""
    opportunity: ArbitrageOpportunity
    hook_template: str       # opening line template, with {placeholders}
    structure: tuple[str, ...]  # bullet outline of the piece
    cta: str                 # call-to-action line
    posting_time_utc: str    # e.g. "Tue/Thu 14:00 UTC"
    estimated_length: str    # e.g. "60 sec video" or "800 word essay"
    why_this_works: str      # one-paragraph rationale


@dataclass(frozen=True)
class NicheContent:
    """Curated per-niche content authored by the seller."""
    niche: str
    title: str               # human-facing pack title
    subtitle: str            # one-line positioning
    platform_hooks: dict[Platform, tuple[str, ...]]
    platform_anti_hooks: dict[Platform, tuple[str, ...]]   # what NOT to do
    format_adaptations: dict[tuple[Format, Format], str]   # src->tgt: instruction
    hot_topics: tuple[str, ...]
    dead_topics: tuple[str, ...]
    emerging_topics: tuple[str, ...]
    edge_audit_questions: tuple[str, ...]
    failure_modes: tuple[str, ...]
    deep_dive_template_by_target: dict[Platform, dict] = field(default_factory=dict)


@dataclass(frozen=True)
class VerticalPack:
    niche: str
    title: str
    subtitle: str
    valid_through: date
    generated_on: date
    arbitrage_opportunities: tuple[ArbitrageOpportunity, ...]
    deep_dives: tuple[DeepDive, ...]
    niche_content: NicheContent


def _deep_dive_for(
    opportunity: ArbitrageOpportunity,
    niche_content: NicheContent,
) -> DeepDive:
    """Construct an execution plan for one opportunity using niche templates."""
    tgt = opportunity.target_platform
    tmpl = niche_content.deep_dive_template_by_target.get(tgt, {})

    hook_choices = niche_content.platform_hooks.get(tgt, ())
    hook = hook_choices[0] if hook_choices else "[customize a hook for this platform]"

    structure = tmpl.get("structure", (
        "Open with the hook above (first 3 seconds / first line).",
        "State the validated insight from source platform.",
        "Translate it into target-platform native form.",
        "Add one specific example with numbers.",
        "Close with the CTA.",
    ))

    cta = tmpl.get("cta", "Ask one specific question that invites a reply.")
    posting_time = tmpl.get("posting_time_utc", "Test 3 slots; track engagement")
    length = tmpl.get("estimated_length", "Native to platform format")

    return DeepDive(
        opportunity=opportunity,
        hook_template=hook,
        structure=tuple(structure),
        cta=cta,
        posting_time_utc=posting_time,
        estimated_length=length,
        why_this_works=(
            f"'{opportunity.topic}' has proven demand on {opportunity.source_platform} "
            f"(engagement {opportunity.demand_at_source:.2f}, sample-validated) but only "
            f"{opportunity.supply_at_target} creators on {opportunity.target_platform}. "
            f"Format adaptation difficulty is {opportunity.difficulty:.2f} — the gap is "
            f"about EFFORT, not RISK. Buyers of this pack who execute within 30 days "
            f"capture the arbitrage before it closes."
        ),
    )


def build_pack(
    niche_content: NicheContent,
    signals: Iterable[PlatformSignal],
    *,
    now: date | None = None,
    max_opportunities: int = 20,
    num_deep_dives: int = 3,
    validity_days: int = 30,
) -> VerticalPack:
    """Build a vertical pack for the given niche.

    Combines EVERGREEN curated content (`niche_content`) with CURRENT live
    arbitrage opportunities derived from `signals`.
    """
    if now is None:
        now = date.today()

    opps = find_opportunities(
        signals, niche=niche_content.niche, max_results=max_opportunities,
    )
    top_for_dive = opps[:num_deep_dives]
    deep_dives = tuple(_deep_dive_for(o, niche_content) for o in top_for_dive)

    return VerticalPack(
        niche=niche_content.niche,
        title=niche_content.title,
        subtitle=niche_content.subtitle,
        generated_on=now,
        valid_through=now + timedelta(days=validity_days),
        arbitrage_opportunities=tuple(opps),
        deep_dives=deep_dives,
        niche_content=niche_content,
    )


# --------------- Markdown renderer ---------------

def _section(title: str) -> str:
    return f"\n## {title}\n"


def _render_opportunities_table(opps: tuple[ArbitrageOpportunity, ...]) -> str:
    lines = [
        "| # | Topic | Source -> Target | Demand | Supply | Score | EV | Difficulty |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for i, o in enumerate(opps, 1):
        lines.append(
            f"| {i} | {o.topic} | {o.source_platform} -> {o.target_platform} "
            f"| {o.demand_at_source:.2f} | {o.supply_at_target} "
            f"| {o.score:.2f} | {o.expected_value:.2f} | {o.difficulty:.2f} |"
        )
    return "\n".join(lines)


def _render_deep_dive(d: DeepDive, idx: int) -> str:
    o = d.opportunity
    lines = [
        f"### Deep dive {idx}: `{o.topic}`",
        "",
        f"**Move:** `{o.source_platform}` -> `{o.target_platform}`  "
        f"(EV {o.expected_value:.2f}, difficulty {o.difficulty:.2f})",
        "",
        "**Hook template:**",
        "",
        f"> {d.hook_template}",
        "",
        "**Structure:**",
    ]
    for i, step in enumerate(d.structure, 1):
        lines.append(f"{i}. {step}")
    lines += [
        "",
        f"**CTA:** {d.cta}",
        f"**Posting window:** {d.posting_time_utc}",
        f"**Length target:** {d.estimated_length}",
        "",
        f"**Why this works:** {d.why_this_works}",
        "",
    ]
    return "\n".join(lines)


def _render_hooks(content: NicheContent) -> str:
    lines = ["### Hooks that work — by platform", ""]
    for plat in PLATFORMS:
        hooks = content.platform_hooks.get(plat, ())
        if not hooks:
            continue
        lines.append(f"**{plat}** ({NATIVE_FORMAT[plat]}):")
        for h in hooks:
            lines.append(f"- {h}")
        lines.append("")
    lines.append("### Anti-hooks — what fails, by platform")
    lines.append("")
    for plat in PLATFORMS:
        antis = content.platform_anti_hooks.get(plat, ())
        if not antis:
            continue
        lines.append(f"**{plat}:**")
        for a in antis:
            lines.append(f"- {a}")
        lines.append("")
    return "\n".join(lines)


def _render_format_adaptations(content: NicheContent) -> str:
    if not content.format_adaptations:
        return ""
    lines = [
        "| Source format | Target format | Adaptation rule |",
        "|---|---|---|",
    ]
    for (src, tgt), rule in content.format_adaptations.items():
        lines.append(f"| {src} | {tgt} | {rule} |")
    return "\n".join(lines)


def _render_topic_lists(content: NicheContent) -> str:
    lines = []
    if content.hot_topics:
        lines.append("### Hot — validated across multiple platforms")
        lines += [f"- {t}" for t in content.hot_topics]
        lines.append("")
    if content.dead_topics:
        lines.append("### Dead — saturated, do not enter")
        lines += [f"- {t}" for t in content.dead_topics]
        lines.append("")
    if content.emerging_topics:
        lines.append("### Emerging — plant a flag this quarter")
        lines += [f"- {t}" for t in content.emerging_topics]
        lines.append("")
    return "\n".join(lines)


def _render_edge_audit(content: NicheContent) -> str:
    lines = [
        "Score yourself: 1 point for every 'yes'. Below is the calibration:",
        "",
        "- **0-7**: GENERALIST. You'll struggle to be referred. Pick one topic and own it for 90 days.",
        "- **8-13**: FOCUSED BUT INDISTINGUISHABLE. You're specialized but using the same language as everyone else.",
        "- **14-17**: REAL EDGE. Double down. Re-run this audit quarterly to catch drift.",
        "- **18-20**: DOMINANT. Stress-test by trying an adjacent niche; you're at risk of complacency.",
        "",
    ]
    for i, q in enumerate(content.edge_audit_questions, 1):
        lines.append(f"{i}. [ ] {q}")
    return "\n".join(lines)


def render_pack_markdown(pack: VerticalPack) -> str:
    """Render the full pack as Markdown — the buyer-facing deliverable."""
    parts = [
        f"# {pack.title}",
        f"_{pack.subtitle}_",
        "",
        f"**Niche:** `{pack.niche}` · **Generated:** {pack.generated_on.isoformat()} · "
        f"**Valid through:** {pack.valid_through.isoformat()}",
        "",
        "---",
        "",
        "## What you get in this pack",
        "",
        "1. **Top 20 cross-platform arbitrage opportunities**, ranked by expected value",
        "2. **3 execution-ready deep dives** — hook, structure, CTA, posting time",
        f"3. **{len(pack.niche_content.platform_hooks)} platform-specific hook libraries** with anti-patterns",
        "4. **Format adaptation matrix** — how to translate content across platforms",
        "5. **Hot / Dead / Emerging topic taxonomy** for your niche",
        "6. **20-question Edge Audit** to score your own differentiation",
        "7. **Honest failure modes** — when this pack will be wrong, and how to detect it",
        "",
        _section("1. Top arbitrage opportunities (CURRENT)"),
        _render_opportunities_table(pack.arbitrage_opportunities),
        "",
        f"_These opportunities are time-sensitive. Re-run after {pack.valid_through.isoformat()}._",
        _section("2. Execution-ready deep dives"),
    ]
    for i, dd in enumerate(pack.deep_dives, 1):
        parts.append(_render_deep_dive(dd, i))

    parts += [
        _section("3. Hook libraries — by platform"),
        _render_hooks(pack.niche_content),
        _section("4. Format adaptation matrix"),
        _render_format_adaptations(pack.niche_content),
        _section("5. Topic taxonomy"),
        _render_topic_lists(pack.niche_content),
        _section("6. Edge Audit — score your own differentiation"),
        _render_edge_audit(pack.niche_content),
        _section("7. Honest failure modes (read this)"),
    ]
    for fm in pack.niche_content.failure_modes:
        parts.append(f"- {fm}")
    parts += [
        "",
        "---",
        "",
        f"Generated by PICKAXE-EDGE. Re-run quarterly to catch platform shifts. "
        f"This pack is valid through {pack.valid_through.isoformat()}; after that, "
        f"the CURRENT arbitrage section (#1) and deep dives (#2) should be regenerated.",
    ]
    return "\n".join(parts)
