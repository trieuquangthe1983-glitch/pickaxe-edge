"""End-to-end smoke: a buyer journey runs end-to-end without errors."""

from core.arbitrage_engine import find_opportunities, opportunities_by_target
from core.edge_scorer import score_creator
from core.niche_analyzer import analyze_niche
from core.pricing import estimate_roi
from core.report import render_full_report
from data.creator_seeds import SAMPLE_CREATORS, peer_set
from data.sources import get_signals, list_niches


def test_full_buyer_journey_for_every_niche():
    for niche in list_niches():
        sigs = get_signals(niche)
        niche_report = analyze_niche(sigs, niche)
        opps = find_opportunities(sigs, niche=niche, max_results=10)
        by_target = opportunities_by_target(opps)
        # Sanity: grouped opps shouldn't exceed total
        assert sum(len(v) for v in by_target.values()) == len(opps)

        md = render_full_report(
            client_name=f"Client-{niche}",
            niche_report=niche_report,
            opportunities=opps,
        )
        assert len(md) > 200, f"Report for {niche} suspiciously short"

    # Also check edge audit + pricing for one creator
    score = score_creator(
        SAMPLE_CREATORS["@basis_trader"],
        peer_set("crypto_trading"),
    )
    assert 0 <= score.overall <= 1

    roi = estimate_roi(audits_per_month=3, retainer_clients=2, saas_pro_subs=10)
    assert roi.monthly_revenue > 0
