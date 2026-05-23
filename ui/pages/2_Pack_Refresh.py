"""Pack Refresh page — buyer-facing.

URL: /Pack_Refresh on the deployed Streamlit app.
Buyer enters their refresh token (issued by seller after Gumroad sale) and
downloads a freshly-generated pack with current arbitrage data.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from datetime import datetime, timezone

import streamlit as st

from core.refresh_token import verify_token
from core.vertical_pack import build_pack, render_pack_markdown
from data.ai_engineering_pack import AI_ENGINEERING_CONTENT
from data.crypto_trading_pack import CRYPTO_TRADING_CONTENT
from data.sources import get_signals


PACKS = {
    "crypto_trading": CRYPTO_TRADING_CONTENT,
    "ai_engineering": AI_ENGINEERING_CONTENT,
}


def _resolve_secret() -> str:
    secret = os.environ.get("PACK_REFRESH_SECRET", "")
    if not secret:
        try:
            secret = st.secrets.get("PACK_REFRESH_SECRET", "")
        except Exception:
            pass
    return secret


st.set_page_config(page_title="Pack Refresh - PICKAXE-EDGE", layout="centered")
st.title("Pack Refresh")
st.caption(
    "Generate a fresh snapshot of your purchased Vertical Pack. "
    "Tokens are issued after purchase via Gumroad / Stripe receipt."
)

secret = _resolve_secret()
if not secret:
    st.error(
        "This refresh page is not configured. The site owner needs to set "
        "`PACK_REFRESH_SECRET` in environment or Streamlit secrets. "
        "If you are a buyer, please contact the seller."
    )
    st.stop()

st.divider()

token_input = st.text_area(
    "Paste your refresh token",
    height=100,
    help="The token was emailed to you after your purchase. Looks like a long random string.",
)

col1, col2 = st.columns(2)
with col1:
    verify_clicked = st.button("Verify token", type="secondary")
with col2:
    st.caption("Don't have a token? Buy a pack at the link in the original email.")

if verify_clicked or token_input:
    token = (token_input or "").strip()
    if not token:
        st.info("Paste a token above and click 'Verify token'.")
        st.stop()

    payload = verify_token(token, secret)
    if payload is None:
        st.error(
            "Token is invalid, tampered with, or expired. "
            "Email the seller with your purchase receipt for a new token."
        )
        st.stop()

    if payload.niche not in PACKS:
        st.error(
            f"Token is valid but for niche '{payload.niche}' which is no longer "
            "available. Contact the seller."
        )
        st.stop()

    expires_dt = datetime.fromtimestamp(payload.expires_at, tz=timezone.utc)
    issued_dt = datetime.fromtimestamp(payload.issued_at, tz=timezone.utc)

    st.success(f"Token verified for {payload.email}")
    m1, m2, m3 = st.columns(3)
    m1.metric("Niche", payload.niche)
    m2.metric("Issued", issued_dt.strftime("%Y-%m-%d"))
    m3.metric("Expires", expires_dt.strftime("%Y-%m-%d"))

    st.divider()

    content = PACKS[payload.niche]
    st.markdown(f"### {content.title}")
    st.caption(content.subtitle)

    validity = st.slider("Pack validity window (days)", 7, 90, 30)
    generate_clicked = st.button("Generate fresh pack", type="primary")

    if generate_clicked:
        with st.spinner("Building pack with current live data..."):
            signals = get_signals(payload.niche)
            pack = build_pack(content, signals, validity_days=int(validity))
            pack_md = render_pack_markdown(pack)

        wc = len(pack_md.split())
        c1, c2, c3 = st.columns(3)
        c1.metric("Word count", f"{wc:,}")
        c2.metric("Opportunities", len(pack.arbitrage_opportunities))
        c3.metric("Valid through", pack.valid_through.isoformat())

        st.download_button(
            "Download fresh pack (Markdown)",
            pack_md,
            file_name=f"pickaxe-pack-{payload.niche}-{pack.generated_on.isoformat()}.md",
            mime="text/markdown",
            type="primary",
        )
        st.info(
            "Save the file. This token remains valid until "
            f"{expires_dt.strftime('%Y-%m-%d')} — re-generate any time."
        )
        with st.expander("Preview the pack"):
            st.markdown(pack_md)
