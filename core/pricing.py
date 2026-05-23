"""Pricing & ROI calculator for the productized service layer.

Used by the UI's 'Quote builder' tab and embedded into client reports.
"""

from __future__ import annotations

from dataclasses import dataclass

# Service tiers — the actual revenue layer (not the SaaS layer)
TIERS = {
    "audit_500": {
        "name": "Arbitrage Audit",
        "price_usd": 500,
        "delivery_days": 5,
        "scope": "1 niche, 1 PDF report, 20 ranked opportunities, no revisions",
    },
    "strategy_2000": {
        "name": "90-Day Niche Strategy",
        "price_usd": 2000,
        "delivery_days": 10,
        "scope": "1 niche, 90-day content calendar, 2 revisions, 1 strategy call",
    },
    "retainer_299": {
        "name": "Monthly Arbitrage Briefing",
        "price_usd": 299,
        "delivery_days": 30,  # per cycle
        "scope": "Monthly refresh, top 10 new opportunities, Slack channel access",
    },
    "saas_pro_49": {
        "name": "SaaS Pro (self-serve)",
        "price_usd": 49,
        "delivery_days": 0,
        "scope": "Unlimited scans, edge audits, 1 user",
    },
    "saas_agency_299": {
        "name": "SaaS Agency (white-label)",
        "price_usd": 299,
        "delivery_days": 0,
        "scope": "Multi-niche, multi-client, white-label report PDFs",
    },
}


@dataclass(frozen=True)
class ROIEstimate:
    monthly_revenue: float
    annual_revenue: float
    annual_cogs: float           # API/tool/labor costs
    annual_profit: float
    margin_pct: float
    breakeven_clients: int       # min clients needed to cover monthly fixed costs
    assumptions: tuple[str, ...]


def estimate_roi(
    *,
    audits_per_month: int = 0,
    strategies_per_month: int = 0,
    retainer_clients: int = 0,
    saas_pro_subs: int = 0,
    saas_agency_subs: int = 0,
    monthly_fixed_cost: float = 200.0,  # API + hosting + tools baseline
    labor_hours_per_audit: float = 6.0,
    labor_rate_usd: float = 50.0,
) -> ROIEstimate:
    """Compute simple ROI given a mix of service/SaaS volume."""
    monthly_revenue = (
        audits_per_month * TIERS["audit_500"]["price_usd"]
        + strategies_per_month * TIERS["strategy_2000"]["price_usd"]
        + retainer_clients * TIERS["retainer_299"]["price_usd"]
        + saas_pro_subs * TIERS["saas_pro_49"]["price_usd"]
        + saas_agency_subs * TIERS["saas_agency_299"]["price_usd"]
    )
    annual_revenue = monthly_revenue * 12

    labor_cost_per_audit = labor_hours_per_audit * labor_rate_usd
    labor_cost_per_strategy = labor_hours_per_audit * 3 * labor_rate_usd  # 3x audit effort
    labor_cost_per_retainer = labor_hours_per_audit * 0.5 * labor_rate_usd  # half-day per cycle

    annual_labor = (
        audits_per_month * labor_cost_per_audit
        + strategies_per_month * labor_cost_per_strategy
        + retainer_clients * labor_cost_per_retainer
    ) * 12
    annual_cogs = monthly_fixed_cost * 12 + annual_labor
    annual_profit = annual_revenue - annual_cogs
    margin_pct = (annual_profit / annual_revenue * 100.0) if annual_revenue > 0 else 0.0

    avg_audit_revenue = TIERS["audit_500"]["price_usd"]
    breakeven_clients = (
        int(monthly_fixed_cost / avg_audit_revenue) + 1
        if avg_audit_revenue > 0 else 0
    )

    return ROIEstimate(
        monthly_revenue=round(monthly_revenue, 2),
        annual_revenue=round(annual_revenue, 2),
        annual_cogs=round(annual_cogs, 2),
        annual_profit=round(annual_profit, 2),
        margin_pct=round(margin_pct, 2),
        breakeven_clients=breakeven_clients,
        assumptions=(
            f"Labor: {labor_hours_per_audit}h/audit @ ${labor_rate_usd}/h",
            f"Fixed monthly cost: ${monthly_fixed_cost}",
            "Strategy = 3x audit effort; Retainer = 0.5x audit effort per cycle",
            "No taxes/payment-processor fees included",
        ),
    )
