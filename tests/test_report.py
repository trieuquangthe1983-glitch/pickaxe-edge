"""Report renderer produces valid Markdown with required sections."""

from core.arbitrage_engine import find_opportunities
from core.edge_scorer import score_creator
from core.niche_analyzer import analyze_niche
from core.report import (
    render_arbitrage_section,
    render_edge_section,
    render_full_report,
    render_niche_section,
)
from data.creator_seeds import SAMPLE_CREATORS, peer_set
from data.sources import get_signals


def test_full_report_contains_all_sections():
    sigs = get_signals("crypto_trading")
    report = analyze_niche(sigs, "crypto_trading")
    opps = find_opportunities(sigs, niche="crypto_trading", max_results=5)
    score = score_creator(
        SAMPLE_CREATORS["@basis_trader"],
        peer_set("crypto_trading"),
    )
    md = render_full_report(
        client_name="Acme Creators",
        niche_report=report,
        opportunities=opps,
        edge_handle="@basis_trader",
        edge_score=score,
    )
    assert "# PICKAXE-EDGE report — Acme Creators" in md
    assert "## Executive summary" in md
    assert "## Niche overview" in md
    assert "## Top arbitrage opportunities" in md
    assert "## Edge audit" in md
    assert "Rationale" in md


def test_report_handles_no_opportunities_gracefully():
    sigs = get_signals("crypto_trading")
    report = analyze_niche(sigs, "crypto_trading")
    md = render_full_report(
        client_name="X",
        niche_report=report,
        opportunities=[],
    )
    assert "No arbitrage opportunities found" in md
    assert "## Top arbitrage opportunities" not in md


def test_arbitrage_section_renders_table():
    sigs = get_signals("longevity")
    opps = find_opportunities(sigs, niche="longevity", max_results=3)
    md = render_arbitrage_section(opps)
    assert "| Topic |" in md
    # one header row + separator + N data rows
    assert md.count("\n|") >= len(opps) + 2


def test_niche_section_lists_all_platforms():
    sigs = get_signals("ai_engineering")
    report = analyze_niche(sigs, "ai_engineering")
    md = render_niche_section(report)
    for plat in ("youtube", "tiktok", "twitter", "linkedin", "reddit", "substack"):
        assert plat in md


def test_edge_section_includes_verdict():
    score = score_creator(
        SAMPLE_CREATORS["@basis_trader"],
        peer_set("crypto_trading"),
    )
    md = render_edge_section("@basis_trader", score)
    assert "**Verdict:**" in md
    assert score.verdict in md
