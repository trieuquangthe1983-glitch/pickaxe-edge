"""Pricing & ROI math."""

from core.pricing import TIERS, estimate_roi


def test_all_tiers_have_required_fields():
    for key, tier in TIERS.items():
        assert "name" in tier
        assert "price_usd" in tier
        assert "delivery_days" in tier
        assert "scope" in tier
        assert tier["price_usd"] > 0


def test_zero_volume_zero_revenue():
    roi = estimate_roi()
    assert roi.monthly_revenue == 0
    assert roi.annual_revenue == 0
    assert roi.annual_profit < 0  # still paying fixed costs


def test_audit_only_roi_basic():
    roi = estimate_roi(audits_per_month=2)
    assert roi.monthly_revenue == 1000.0
    assert roi.annual_revenue == 12000.0
    # Labor: 2 audits/mo * 6h * $50 = $600/mo = $7200/yr; fixed = $2400/yr
    assert roi.annual_cogs == 7200.0 + 2400.0
    assert roi.annual_profit == 12000.0 - 9600.0


def test_mixed_tier_revenue_sums():
    roi = estimate_roi(
        audits_per_month=1, strategies_per_month=1,
        retainer_clients=3, saas_pro_subs=10,
    )
    expected = 500 + 2000 + 3 * 299 + 10 * 49
    assert roi.monthly_revenue == expected


def test_breakeven_clients_reasonable():
    roi = estimate_roi(monthly_fixed_cost=500)
    # Need to cover $500 fixed with $500 audits -> 2 audits gives margin, 1 too tight
    assert roi.breakeven_clients == 2


def test_margin_positive_at_realistic_volume():
    roi = estimate_roi(audits_per_month=4, retainer_clients=5, saas_pro_subs=20)
    assert roi.annual_profit > 0
    assert roi.margin_pct > 0
