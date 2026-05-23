"""Vertical pack generator + niche-content tests (crypto + ai_engineering)."""

import pytest
from datetime import date

from core.types import PLATFORMS
from core.vertical_pack import build_pack, render_pack_markdown
from data.crypto_trading_pack import CRYPTO_TRADING_CONTENT
from data.ai_engineering_pack import AI_ENGINEERING_CONTENT
from data.sources import get_signals


SEED_DATE = date(2026, 5, 23)

# Run the structural tests against every shipped pack
ALL_PACKS = [CRYPTO_TRADING_CONTENT, AI_ENGINEERING_CONTENT]


@pytest.mark.parametrize("content", ALL_PACKS, ids=lambda c: c.niche)
def test_pack_has_hooks_for_all_six_platforms(content):
    for plat in PLATFORMS:
        assert plat in content.platform_hooks, f"{content.niche}: missing hooks for {plat}"
        assert content.platform_hooks[plat], f"{content.niche}: empty hooks for {plat}"


@pytest.mark.parametrize("content", ALL_PACKS, ids=lambda c: c.niche)
def test_pack_has_anti_hooks_for_all_six_platforms(content):
    for plat in PLATFORMS:
        assert plat in content.platform_anti_hooks, (
            f"{content.niche}: missing anti-hooks for {plat}"
        )


@pytest.mark.parametrize("content", ALL_PACKS, ids=lambda c: c.niche)
def test_pack_has_exactly_20_edge_audit_questions(content):
    assert len(content.edge_audit_questions) == 20, (
        f"{content.niche}: edge audit has {len(content.edge_audit_questions)} questions, need exactly 20"
    )


@pytest.mark.parametrize("content", ALL_PACKS, ids=lambda c: c.niche)
def test_pack_has_at_least_5_hot_dead_emerging_each(content):
    assert len(content.hot_topics) >= 5
    assert len(content.dead_topics) >= 5
    assert len(content.emerging_topics) >= 5


@pytest.mark.parametrize("content", ALL_PACKS, ids=lambda c: c.niche)
def test_pack_has_failure_modes(content):
    assert len(content.failure_modes) >= 5


def test_build_pack_returns_correct_validity_window():
    sigs = get_signals("crypto_trading")
    pack = build_pack(CRYPTO_TRADING_CONTENT, sigs, now=SEED_DATE, validity_days=30)
    assert pack.generated_on == SEED_DATE
    assert (pack.valid_through - pack.generated_on).days == 30


def test_build_pack_caps_opportunities_and_deep_dives():
    sigs = get_signals("crypto_trading")
    pack = build_pack(
        CRYPTO_TRADING_CONTENT, sigs,
        now=SEED_DATE, max_opportunities=15, num_deep_dives=3,
    )
    assert len(pack.arbitrage_opportunities) <= 15
    assert len(pack.deep_dives) == 3


def test_deep_dives_include_target_platform_template_when_available():
    """Each deep dive should use the platform-specific template if defined."""
    sigs = get_signals("crypto_trading")
    pack = build_pack(CRYPTO_TRADING_CONTENT, sigs, now=SEED_DATE)
    for dd in pack.deep_dives:
        tgt = dd.opportunity.target_platform
        if tgt in CRYPTO_TRADING_CONTENT.deep_dive_template_by_target:
            template_struct = CRYPTO_TRADING_CONTENT.deep_dive_template_by_target[tgt]["structure"]
            assert dd.structure == template_struct, (
                f"deep dive for target {tgt} did not use the curated template"
            )


def test_render_pack_markdown_contains_all_sections():
    sigs = get_signals("crypto_trading")
    pack = build_pack(CRYPTO_TRADING_CONTENT, sigs, now=SEED_DATE)
    md = render_pack_markdown(pack)
    assert CRYPTO_TRADING_CONTENT.title in md
    assert "1. Top arbitrage opportunities" in md
    assert "2. Execution-ready deep dives" in md
    assert "3. Hook libraries" in md
    assert "4. Format adaptation matrix" in md
    assert "5. Topic taxonomy" in md
    assert "6. Edge Audit" in md
    assert "7. Honest failure modes" in md
    assert pack.valid_through.isoformat() in md


def test_render_pack_lists_at_least_one_opportunity():
    sigs = get_signals("crypto_trading")
    pack = build_pack(CRYPTO_TRADING_CONTENT, sigs, now=SEED_DATE)
    assert len(pack.arbitrage_opportunities) > 0


@pytest.mark.parametrize("content", ALL_PACKS, ids=lambda c: c.niche)
def test_pack_total_word_count_above_minimum_for_99_usd_product(content):
    """Buyer-quality threshold: a $99 pack must feel substantial. Aim 2500+ words."""
    sigs = get_signals(content.niche)
    pack = build_pack(content, sigs, now=SEED_DATE)
    md = render_pack_markdown(pack)
    words = len(md.split())
    assert words >= 2500, f"{content.niche} pack is only {words} words — too thin for $99"


@pytest.mark.parametrize("content", ALL_PACKS, ids=lambda c: c.niche)
def test_no_external_urls_in_pack_body(content):
    """The pack should NOT contain external URLs that could rot or look spammy."""
    sigs = get_signals(content.niche)
    pack = build_pack(content, sigs, now=SEED_DATE)
    md = render_pack_markdown(pack)
    assert "https://" not in md, f"{content.niche}: external URLs should not appear"


@pytest.mark.parametrize("content", ALL_PACKS, ids=lambda c: c.niche)
def test_edge_audit_questions_are_yes_no_phrased(content):
    """All 20 questions should be answerable yes/no — they're a checklist."""
    for q in content.edge_audit_questions:
        first_word = q.split()[0].lower()
        assert first_word in {"can", "do", "does", "has", "have", "is", "are", "was", "were"}, (
            f"{content.niche}: question '{q[:60]}...' doesn't start with a yes/no verb"
        )
