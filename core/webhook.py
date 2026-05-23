"""Gumroad Ping webhook handler — framework-agnostic core logic.

Gumroad's "Ping" sends a form-encoded HTTP POST to your configured URL on every
sale. It does NOT cryptographically sign the payload by default. The practical
security model used here:

1. **Shared secret in URL query param**: Gumroad's webhook URL is configured as
   `https://your-webhook.app/gumroad?key=SECRET`. The handler verifies `key`
   matches `GUMROAD_WEBHOOK_SECRET` env var via constant-time compare.
2. **Seller-ID match**: optionally pin to your exact seller_id so even a
   leaked secret can't be abused by random Gumroad accounts.
3. **Product-permalink allowlist**: only the products we know map to a niche
   produce tokens; unknown products return 400 fast.

For HMAC-signed webhooks, migrate to Gumroad's Resource Subscriptions API
(separate product, not covered here).
"""

from __future__ import annotations

import hmac as _hmac
from dataclasses import dataclass
from typing import Callable

from core.refresh_token import generate_token

# Gumroad permalink -> niche. Set the LEFT side to YOUR product's URL slug
# (the part after gumroad.com/l/). Default set is illustrative.
DEFAULT_PRODUCT_TO_NICHE: dict[str, str] = {
    "pickaxe-crypto":   "crypto_trading",
    "pickaxe-ai-eng":   "ai_engineering",
    "pickaxe-saas":     "indie_saas",
}


@dataclass(frozen=True)
class WebhookResult:
    ok: bool
    reason: str
    email: str | None = None
    niche: str | None = None
    token: str | None = None


# (to_email, subject, body) -> None. Raise on failure.
EmailSender = Callable[[str, str, str], None]


def _norm(s: object) -> str:
    return (s if isinstance(s, str) else "").strip()


def handle_gumroad_ping(
    payload: dict,
    *,
    shared_secret: str,
    submitted_secret: str,
    pack_secret: str,
    expected_seller_id: str | None = None,
    email_sender: EmailSender | None = None,
    app_url: str = "https://YOUR-APP.streamlit.app",
    product_to_niche: dict[str, str] | None = None,
    token_valid_days: int = 90,
) -> WebhookResult:
    """Process one Gumroad Ping payload. Idempotent on bad inputs.

    Args:
        payload: form data dict from Gumroad. Expected keys: email, permalink
            (or product_permalink), seller_id, sale_id.
        shared_secret: the configured webhook secret on this server.
        submitted_secret: the secret the caller supplied (e.g. from ?key= query).
        pack_secret: PACK_REFRESH_SECRET used to sign the issued token.
        expected_seller_id: if set, payload's seller_id MUST match.
        email_sender: callable to deliver the token to buyer. None = skip email.
        app_url: included in the email body so buyer knows where to go.
        product_to_niche: override product->niche map.
        token_valid_days: token expiry window.
    """
    # 1. Auth
    if not shared_secret or not submitted_secret:
        return WebhookResult(False, "missing webhook secret")
    if not _hmac.compare_digest(shared_secret, submitted_secret):
        return WebhookResult(False, "wrong webhook secret")

    # 2. Seller pin (optional but recommended)
    seller_id = _norm(payload.get("seller_id"))
    if expected_seller_id and seller_id != expected_seller_id:
        return WebhookResult(False, f"seller_id mismatch: got {seller_id!r}")

    # 3. Email present + valid-looking
    email = _norm(payload.get("email")).lower()
    if not email or "@" not in email:
        return WebhookResult(False, "invalid or missing email")

    # 4. Product permalink -> niche
    permalink = (
        _norm(payload.get("permalink"))
        or _norm(payload.get("product_permalink"))
    )
    mapping = product_to_niche or DEFAULT_PRODUCT_TO_NICHE
    niche = mapping.get(permalink)
    if not niche:
        return WebhookResult(
            False, f"unknown product permalink: {permalink!r}",
            email=email,
        )

    # 5. Issue token
    if not pack_secret:
        return WebhookResult(False, "PACK_REFRESH_SECRET not configured",
                             email=email, niche=niche)
    try:
        token = generate_token(
            email, niche, pack_secret, valid_days=token_valid_days,
        )
    except ValueError as e:
        return WebhookResult(False, f"token generation failed: {e}",
                             email=email, niche=niche)

    # 6. Deliver email (best-effort — if it fails we still consider the
    # webhook "successful" because Gumroad will retry on non-2xx, and a
    # duplicate token issuance is fine; but caller can see email_sent=False
    # via the reason field).
    email_status = "ok (no sender configured)"
    if email_sender is not None:
        try:
            email_sender(
                email,
                f"Your PICKAXE-EDGE pack access: {niche}",
                _compose_email_body(
                    niche=niche, app_url=app_url,
                    token=token, valid_days=token_valid_days,
                ),
            )
            email_status = "sent"
        except Exception as e:
            email_status = f"send failed: {e}"

    return WebhookResult(
        True, f"token issued; email: {email_status}",
        email=email, niche=niche, token=token,
    )


def _compose_email_body(*, niche: str, app_url: str, token: str, valid_days: int) -> str:
    return (
        f"Thanks for your purchase!\n\n"
        f"Your {niche} pack is ready. To download or regenerate it with current "
        f"data any time within the next {valid_days} days, go to:\n\n"
        f"  {app_url}/Pack_Refresh\n\n"
        f"And paste this refresh token:\n\n"
        f"  {token}\n\n"
        f"Token validity: {valid_days} days from now. "
        f"After that, re-purchase the $49 refresh on Gumroad for another window.\n\n"
        f"Questions: just reply to this email.\n"
    )
