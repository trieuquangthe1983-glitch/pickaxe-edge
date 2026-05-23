"""Buyer Dashboard page — at /Buyer_Dashboard on the deployed Streamlit app.

Buyers paste one or more refresh tokens, see all their entitlements at a
glance, regenerate any pack with fresh data, and see clearly which packs
they don't own yet (with buy links).

Honest scope: this is a STATELESS dashboard. We do not store purchase or
refresh history — that would require a database, and Streamlit Cloud's
ephemeral storage means files don't persist between app restarts. Refresh
history within ONE session is tracked in st.session_state.

For a full persistent dashboard (history across sessions, total downloads
metric, expiry warnings via email), migrate to a backend with a real DB
(Turso, Neon, Supabase). Listed in NEXT_STEPS as future work.
"""

from __future__ import annotations

import os
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import streamlit as st

from core.refresh_token import TokenPayload, verify_token
from core.vertical_pack import build_pack, render_pack_markdown
from data.ai_engineering_pack import AI_ENGINEERING_CONTENT
from data.crypto_trading_pack import CRYPTO_TRADING_CONTENT
from data.indie_saas_pack import INDIE_SAAS_CONTENT
from data.sources import get_signals


PACKS = {
    "crypto_trading": CRYPTO_TRADING_CONTENT,
    "ai_engineering": AI_ENGINEERING_CONTENT,
    "indie_saas":     INDIE_SAAS_CONTENT,
}

# Gumroad URLs. Update these once you have your real product permalinks.
GUMROAD_BUY_LINKS = {
    "crypto_trading": "https://gumroad.com/l/pickaxe-crypto",
    "ai_engineering": "https://gumroad.com/l/pickaxe-ai-eng",
    "indie_saas":     "https://gumroad.com/l/pickaxe-saas",
}
GUMROAD_REFRESH_LINK = "https://gumroad.com/l/pickaxe-refresh"


def _resolve_secret() -> str:
    secret = os.environ.get("PACK_REFRESH_SECRET", "")
    if not secret:
        try:
            secret = st.secrets.get("PACK_REFRESH_SECRET", "")
        except Exception:
            pass
    return secret


def _verify_many(tokens: list[str], secret: str) -> tuple[list[TokenPayload], list[str]]:
    """Return (valid_payloads, error_messages)."""
    valid: list[TokenPayload] = []
    errors: list[str] = []
    for raw in tokens:
        raw = raw.strip()
        if not raw:
            continue
        p = verify_token(raw, secret)
        if p is None:
            errors.append(f"`{raw[:24]}...` invalid or expired")
        else:
            valid.append(p)
    return valid, errors


def _human_remaining(seconds: int) -> str:
    if seconds < 0:
        return "expired"
    days = seconds // 86400
    if days > 1:
        return f"{days} days"
    hours = seconds // 3600
    return f"{hours} hours"


st.set_page_config(page_title="Buyer Dashboard - PICKAXE-EDGE", layout="wide")
st.title("Buyer Dashboard")
st.caption(
    "View all your purchased packs at a glance. Paste one token per line for each pack "
    "you own. Tokens were emailed to you after purchase."
)

secret = _resolve_secret()
if not secret:
    st.error(
        "This dashboard is not configured. The site owner needs to set "
        "`PACK_REFRESH_SECRET`. If you're a buyer, contact the seller."
    )
    st.stop()

# Init session-state refresh log
if "refresh_log" not in st.session_state:
    st.session_state.refresh_log = []  # list of (timestamp_iso, niche, words)

token_text = st.text_area(
    "Your refresh tokens (one per line)",
    height=130,
    help="Paste all tokens you've received. Each token unlocks one niche. Stored only in this browser session.",
)

if not token_text.strip():
    st.info("Paste at least one token above to see your dashboard.")
    st.markdown("---")
    st.subheader("Not a customer yet?")
    cols = st.columns(len(PACKS))
    for col, (niche, content) in zip(cols, PACKS.items()):
        with col:
            st.markdown(f"**{content.title}**")
            st.caption(content.subtitle[:120] + "...")
            st.link_button(f"Buy {niche} ($99)", GUMROAD_BUY_LINKS[niche])
    st.stop()

tokens = [t for t in token_text.splitlines() if t.strip()]
valid, errors = _verify_many(tokens, secret)

if errors:
    for e in errors:
        st.warning(e)

if not valid:
    st.error("No valid tokens found. Check your purchase email.")
    st.stop()

now_ts = int(datetime.now(timezone.utc).timestamp())

st.subheader("Your entitlements")
ent_cols = st.columns(min(3, len(valid)))
for i, payload in enumerate(valid):
    with ent_cols[i % len(ent_cols)]:
        content = PACKS.get(payload.niche)
        title = content.title if content else f"Unknown ({payload.niche})"
        remaining = _human_remaining(payload.expires_at - now_ts)
        st.markdown(f"### {title}")
        st.caption(f"Owner: `{payload.email}`")
        m1, m2 = st.columns(2)
        m1.metric("Status", "Active" if remaining != "expired" else "Expired")
        m2.metric("Remaining", remaining)

st.markdown("---")
st.subheader("Generate or regenerate your packs")
for payload in valid:
    content = PACKS.get(payload.niche)
    if content is None:
        st.warning(f"Token valid but niche `{payload.niche}` no longer shipped.")
        continue

    with st.expander(f"{content.title}   ({payload.niche})", expanded=False):
        col_a, col_b = st.columns([3, 1])
        with col_a:
            st.caption(content.subtitle)
        with col_b:
            window = st.slider(
                "Validity window (days)", 7, 90, 30,
                key=f"window_{payload.niche}_{payload.email}",
            )

        if st.button(f"Generate fresh {payload.niche} pack", key=f"gen_{payload.niche}_{payload.email}"):
            with st.spinner("Building pack with current data..."):
                signals = get_signals(payload.niche)
                pack = build_pack(content, signals, validity_days=int(window))
                pack_md = render_pack_markdown(pack)

            wc = len(pack_md.split())
            st.session_state.refresh_log.append((
                datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC"),
                payload.niche,
                wc,
            ))

            c1, c2, c3 = st.columns(3)
            c1.metric("Word count", f"{wc:,}")
            c2.metric("Opportunities", len(pack.arbitrage_opportunities))
            c3.metric("Valid through", pack.valid_through.isoformat())

            st.download_button(
                f"Download {payload.niche} pack",
                pack_md,
                file_name=f"pickaxe-pack-{payload.niche}-{pack.generated_on.isoformat()}.md",
                mime="text/markdown",
                type="primary",
                key=f"dl_{payload.niche}_{payload.email}",
            )

st.markdown("---")

# Show packs the buyer does NOT own — soft upsell
owned_niches = {p.niche for p in valid}
unowned = {n: c for n, c in PACKS.items() if n not in owned_niches}
if unowned:
    st.subheader("Add more packs")
    cols = st.columns(len(unowned))
    for col, (niche, content) in zip(cols, unowned.items()):
        with col:
            st.markdown(f"**{content.title}**")
            st.caption(content.subtitle[:140] + ("..." if len(content.subtitle) > 140 else ""))
            st.link_button(f"Buy {niche} ($99)", GUMROAD_BUY_LINKS[niche])

st.markdown("---")
st.subheader("Need a refresh?")
st.caption(
    "Your tokens stay valid for the window shown above. After expiry, "
    "buy a $49 refresh to get a new 90-day token with the latest arbitrage snapshot."
)
st.link_button("Buy pack refresh ($49)", GUMROAD_REFRESH_LINK)

# Session refresh log
if st.session_state.refresh_log:
    st.markdown("---")
    st.subheader("This session's downloads")
    for ts, niche, wc in reversed(st.session_state.refresh_log[-10:]):
        st.text(f"  {ts}  ·  {niche}  ·  {wc:,} words")
    st.caption("This log is only kept for this browser session.")
