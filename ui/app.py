"""PICKAXE-EDGE Streamlit UI — five tabs covering the buyer journey."""

from __future__ import annotations

import sys
from pathlib import Path

# Make project root importable when launched via `streamlit run ui/app.py`
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import pandas as pd
import streamlit as st

from core.arbitrage_engine import find_opportunities, opportunities_by_target
from core.edge_scorer import score_creator
from core.niche_analyzer import analyze_niche
from core.pricing import TIERS, estimate_roi
from core.report import render_full_report
from data.creator_seeds import SAMPLE_CREATORS, peer_set
from data.reddit_source import (
    NICHE_SUBREDDITS,
    refresh_reddit_signals,
    replace_reddit_signals,
)
from data.substack_source import (
    NICHE_PUBLICATIONS,
    refresh_substack_signals,
    replace_substack_signals,
)
from data.youtube_source import (
    estimate_quota_cost,
    refresh_youtube_signals,
    replace_youtube_signals,
)
from data.sources import get_signals, list_niches


def _resolve_youtube_key() -> str:
    """Resolve API key from env var or Streamlit secrets — no hard dependency on either."""
    import os
    key = os.environ.get("YOUTUBE_API_KEY", "")
    if not key:
        try:
            key = st.secrets.get("YOUTUBE_API_KEY", "")
        except Exception:
            pass
    return key


st.set_page_config(page_title="PICKAXE-EDGE", page_icon=None, layout="wide")

st.title("PICKAXE-EDGE")
st.caption(
    "Contrarian pickaxe play for the creator economy. "
    "Find content arbitrage opportunities, quantify edge, price the service."
)

with st.sidebar:
    st.header("Configuration")
    niche = st.selectbox("Niche", list_niches(), index=0)
    demand_floor = st.slider("Demand floor (source platform)", 0.0, 1.0, 0.55, 0.05)
    supply_ceiling = st.slider("Supply ceiling (target platform)", 0, 30, 8)
    max_results = st.slider("Max opportunities", 5, 30, 15)

    st.divider()
    st.markdown("**Live data sources**")
    use_live_reddit = st.toggle(
        "Use live Reddit",
        value=False,
        help="Replaces mock Reddit signals with public Reddit JSON API. ~5-20s.",
    )
    reddit_time_filter = st.selectbox(
        "Reddit window", ["week", "month", "year"], index=1, disabled=not use_live_reddit,
    )
    use_live_substack = st.toggle(
        "Use live Substack",
        value=False,
        help="Replaces mock Substack signals with public RSS. NOTE: engagement is a supply-proxy (RSS lacks like/comment data).",
    )
    substack_days = st.slider(
        "Substack window (days)", 7, 90, 30, disabled=not use_live_substack,
    )
    yt_key_present = bool(_resolve_youtube_key())
    use_live_youtube = st.toggle(
        "Use live YouTube",
        value=False,
        disabled=not yt_key_present,
        help=("Requires YOUTUBE_API_KEY in env or .streamlit/secrets.toml. "
              "Costs ~150 quota units per topic; free tier = 10k/day."),
    )
    if not yt_key_present:
        st.caption("Set YOUTUBE_API_KEY to enable. See docs/DEPLOY.md.")
    youtube_days = st.slider(
        "YouTube window (days)", 7, 90, 30, disabled=not use_live_youtube,
    )

    st.divider()
    st.markdown("**Pricing tiers**")
    for key, t in TIERS.items():
        st.caption(f"**{t['name']}** - ${t['price_usd']}")


@st.cache_data(ttl=3600, show_spinner="Fetching live data (this can take 10-30s)...")
def _signals_for(
    niche: str,
    use_live_reddit: bool,
    reddit_time_filter: str,
    use_live_substack: bool,
    substack_days: int,
    use_live_youtube: bool,
    youtube_days: int,
):
    sigs = get_signals(niche)
    if use_live_reddit and niche in NICHE_SUBREDDITS:
        reddit_topics = sorted({s.topic for s in sigs if s.platform == "reddit"})
        try:
            live = refresh_reddit_signals(niche, reddit_topics, time_filter=reddit_time_filter)
            if live:
                sigs = replace_reddit_signals(sigs, live, niche)
        except Exception as e:
            st.warning(f"Live Reddit fetch failed: {e}. Using mock Reddit data.")
    if use_live_substack and niche in NICHE_PUBLICATIONS:
        substack_topics = sorted({s.topic for s in sigs if s.platform == "substack"})
        try:
            live = refresh_substack_signals(
                niche, substack_topics, days_window=substack_days,
            )
            if live:
                sigs = replace_substack_signals(sigs, live, niche)
        except Exception as e:
            st.warning(f"Live Substack fetch failed: {e}. Using mock Substack data.")
    if use_live_youtube:
        yt_key = _resolve_youtube_key()
        if yt_key:
            youtube_topics = sorted({s.topic for s in sigs if s.platform == "youtube"})
            est = estimate_quota_cost(len(youtube_topics))
            st.caption(f"YouTube quota estimate: ~{est} units ({len(youtube_topics)} topics).")
            try:
                live = refresh_youtube_signals(
                    niche, youtube_topics,
                    api_key=yt_key, days_window=youtube_days,
                )
                if live:
                    sigs = replace_youtube_signals(sigs, live, niche)
            except Exception as e:
                st.warning(f"Live YouTube fetch failed: {e}. Using mock YouTube data.")
    return sigs


tab_niche, tab_arb, tab_edge, tab_pricing, tab_report = st.tabs([
    "1. Niche scan", "2. Arbitrage opportunities", "3. Edge audit",
    "4. Quote builder", "5. Client report",
])


# ---------------- TAB 1: NICHE SCAN ----------------
with tab_niche:
    st.subheader(f"Niche scan: `{niche}`")
    sigs = _signals_for(
        niche,
        use_live_reddit, reddit_time_filter,
        use_live_substack, substack_days,
        use_live_youtube, youtube_days,
    )
    report = analyze_niche(sigs, niche)

    rows = []
    for s in report.summaries:
        rows.append({
            "Platform": s.platform,
            "Topics": s.topic_count,
            "Avg engagement": round(s.avg_engagement, 3),
            "Total supply (creators)": s.total_supply,
            "Saturation": s.saturation,
            "Top topics": ", ".join(s.top_topics) if s.top_topics else "-",
        })
    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("**Recommended SOURCE platforms** (demand validated)")
        for p in report.recommended_source_platforms or ("-",):
            st.write(f"- {p}")
    with col_b:
        st.markdown("**Recommended TARGET platforms** (under-supplied)")
        for p in report.recommended_target_platforms or ("-",):
            st.write(f"- {p}")


# ---------------- TAB 2: ARBITRAGE ----------------
with tab_arb:
    st.subheader(f"Arbitrage opportunities: `{niche}`")
    sigs = _signals_for(
        niche,
        use_live_reddit, reddit_time_filter,
        use_live_substack, substack_days,
        use_live_youtube, youtube_days,
    )
    opps = find_opportunities(
        sigs, niche=niche,
        demand_floor=demand_floor,
        supply_ceiling=supply_ceiling,
        max_results=max_results,
    )

    if not opps:
        st.warning("No arbitrage found at current thresholds. Try lowering the demand floor.")
    else:
        df = pd.DataFrame([{
            "#": i + 1,
            "Topic": o.topic,
            "Source": o.source_platform,
            "Target": o.target_platform,
            "Demand@source": o.demand_at_source,
            "Supply@target": o.supply_at_target,
            "Score": o.score,
            "Difficulty": o.difficulty,
            "EV": round(o.expected_value, 4),
        } for i, o in enumerate(opps)])
        st.dataframe(df, use_container_width=True, hide_index=True)

        st.markdown("---")
        st.markdown("### Opportunities grouped by TARGET platform")
        grouped = opportunities_by_target(opps)
        if grouped:
            target_choice = st.selectbox(
                "Inspect target platform", sorted(grouped.keys()), key="target_select",
            )
            for o in grouped[target_choice]:
                with st.expander(f"{o.topic}  -  EV {o.expected_value:.2f}  (from {o.source_platform})"):
                    st.write(o.rationale)


# ---------------- TAB 3: EDGE AUDIT ----------------
with tab_edge:
    st.subheader("Edge audit — quantify creator differentiation")
    handle = st.selectbox(
        "Sample creator",
        list(SAMPLE_CREATORS.keys()),
        help="Mock profiles. In production, ingest the creator's last 90 days of content.",
    )
    profile = SAMPLE_CREATORS[handle]
    peers = peer_set(profile.niche)
    score = score_creator(profile, peers)

    col1, col2, col3 = st.columns(3)
    col1.metric("Overall edge", f"{score.overall:.2f}")
    col2.metric("Vocabulary uniqueness", f"{score.vocabulary_uniqueness:.2f}")
    col3.metric("Topic concentration", f"{score.topic_concentration:.2f}")

    col4, col5, col6 = st.columns(3)
    col4.metric("Audience cohesion", f"{score.audience_cohesion:.2f}")
    col5.metric("Engagement depth", f"{score.engagement_depth:.2f}")
    col6.metric("Hook repeatability", f"{score.hook_repeatability:.2f}")

    st.info(f"**Verdict:** {score.verdict}")

    with st.expander("Profile detail"):
        st.json({
            "handle": profile.handle,
            "niche": profile.niche,
            "topics": list(profile.topics),
            "topic_weights": list(profile.topic_weights),
            "vocabulary_sample": sorted(profile.vocabulary)[:10],
            "avg_engagement": profile.avg_engagement,
            "comments_per_like": profile.comments_per_like,
        })


# ---------------- TAB 4: QUOTE BUILDER ----------------
with tab_pricing:
    st.subheader("Quote builder — productized service economics")
    col_a, col_b = st.columns(2)
    with col_a:
        audits = st.number_input("Audits per month ($500 each)", 0, 50, 3)
        strategies = st.number_input("Strategies per month ($2,000 each)", 0, 20, 1)
        retainers = st.number_input("Retainer clients ($299/mo each)", 0, 100, 5)
    with col_b:
        pro_subs = st.number_input("SaaS Pro subs ($49/mo each)", 0, 500, 20)
        agency_subs = st.number_input("SaaS Agency subs ($299/mo each)", 0, 100, 2)
        fixed_cost = st.number_input("Monthly fixed cost ($)", 0, 5000, 200)

    roi = estimate_roi(
        audits_per_month=int(audits),
        strategies_per_month=int(strategies),
        retainer_clients=int(retainers),
        saas_pro_subs=int(pro_subs),
        saas_agency_subs=int(agency_subs),
        monthly_fixed_cost=float(fixed_cost),
    )

    m1, m2, m3 = st.columns(3)
    m1.metric("Monthly revenue", f"${roi.monthly_revenue:,.0f}")
    m2.metric("Annual profit", f"${roi.annual_profit:,.0f}",
              delta=f"{roi.margin_pct:.1f}% margin")
    m3.metric("Breakeven audits/mo", str(roi.breakeven_clients))

    st.caption("Assumptions:")
    for a in roi.assumptions:
        st.caption(f"- {a}")


# ---------------- TAB 5: CLIENT REPORT ----------------
with tab_report:
    st.subheader("Client-ready Markdown report")
    client_name = st.text_input("Client name", "Acme Creators LLC")
    include_edge = st.checkbox("Include edge audit section", value=True)
    edge_handle = (
        st.selectbox("Edge audit subject", list(SAMPLE_CREATORS.keys()), key="report_edge_handle")
        if include_edge else None
    )

    sigs = _signals_for(
        niche,
        use_live_reddit, reddit_time_filter,
        use_live_substack, substack_days,
        use_live_youtube, youtube_days,
    )
    niche_report = analyze_niche(sigs, niche)
    opps = find_opportunities(
        sigs, niche=niche,
        demand_floor=demand_floor,
        supply_ceiling=supply_ceiling,
        max_results=max_results,
    )
    edge_score = None
    if edge_handle:
        profile = SAMPLE_CREATORS[edge_handle]
        edge_score = score_creator(profile, peer_set(profile.niche))

    md = render_full_report(
        client_name=client_name,
        niche_report=niche_report,
        opportunities=opps,
        edge_handle=edge_handle,
        edge_score=edge_score,
    )
    st.download_button(
        "Download Markdown",
        md,
        file_name=f"pickaxe-edge-{niche}-{client_name.replace(' ', '_')}.md",
        mime="text/markdown",
    )
    st.markdown(md)
