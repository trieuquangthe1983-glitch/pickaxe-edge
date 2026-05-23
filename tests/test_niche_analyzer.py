"""Niche analyzer summarizes correctly per-platform."""

from core.niche_analyzer import analyze_niche
from data.sources import get_signals, list_niches


def test_analyze_covers_all_platforms_even_if_zero_signal():
    sigs = get_signals("crypto_trading")
    report = analyze_niche(sigs, "crypto_trading")
    platforms = {s.platform for s in report.summaries}
    assert platforms == {"youtube", "tiktok", "twitter", "linkedin", "reddit", "substack"}


def test_recommended_sources_have_topics():
    sigs = get_signals("ai_engineering")
    report = analyze_niche(sigs, "ai_engineering")
    assert len(report.recommended_source_platforms) > 0
    for plat in report.recommended_source_platforms:
        summary = next(s for s in report.summaries if s.platform == plat)
        assert summary.topic_count > 0


def test_recommended_targets_are_not_saturated():
    sigs = get_signals("indie_saas")
    report = analyze_niche(sigs, "indie_saas")
    for plat in report.recommended_target_platforms:
        summary = next(s for s in report.summaries if s.platform == plat)
        assert summary.saturation != "saturated"


def test_analyze_works_for_every_seeded_niche():
    sigs = get_signals()
    for niche in list_niches():
        report = analyze_niche(sigs, niche)
        assert report.niche == niche
        # At least some platforms have data for every seeded niche
        assert any(s.topic_count > 0 for s in report.summaries)
