"""HMAC-signed refresh tokens for $49 pack refresh distribution.

Architecture:
- Seller issues a token via `scripts/issue_token.py` after Gumroad/Stripe
  reports a paid sale. Pass the token to the buyer (email, Gumroad receipt
  message, Stripe success_url query param, etc.).
- Buyer pastes the token into `/Pack_Refresh` Streamlit page. We verify the
  signature with the same `PACK_REFRESH_SECRET` env var and serve a freshly
  generated pack.
- No database, no auth provider, no third-party. Token is self-contained.
- If the secret leaks, all outstanding tokens are forgeable — rotate by
  changing `PACK_REFRESH_SECRET` and re-issuing tokens for active customers.

Token format (base64-urlsafe encoded):
  email|niche|issued_at|expires_at|signature
where signature = HMAC-SHA256(secret, "email|niche|issued_at|expires_at")[:24]
"""

from __future__ import annotations

import base64
import hashlib
import hmac
import time
from dataclasses import dataclass


_SIG_LEN = 24  # hex chars; 96 bits of entropy — well above brute-force


@dataclass(frozen=True)
class TokenPayload:
    email: str
    niche: str
    issued_at: int   # unix epoch seconds
    expires_at: int  # unix epoch seconds


def _sign(body: str, secret: str) -> str:
    return hmac.new(
        secret.encode("utf-8"),
        body.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()[:_SIG_LEN]


def generate_token(
    email: str,
    niche: str,
    secret: str,
    *,
    valid_days: int = 90,
    now: int | None = None,
) -> str:
    """Issue a refresh token for a buyer.

    Args:
        email: buyer email (will be lowercased + stripped)
        niche: which pack they purchased (e.g. "crypto_trading")
        secret: PACK_REFRESH_SECRET — must match what verifier uses
        valid_days: token expiry window. Default 90 = 1 quarter.
        now: unix seconds — inject for deterministic tests.

    Raises:
        ValueError if secret missing or email invalid.
    """
    if not secret:
        raise ValueError("secret is required")
    email = (email or "").strip().lower()
    if not email or "@" not in email or "|" in email:
        raise ValueError(f"invalid email: {email!r}")
    if not niche or "|" in niche:
        raise ValueError(f"invalid niche: {niche!r}")
    if now is None:
        now = int(time.time())
    expires = now + int(valid_days) * 86400
    body = f"{email}|{niche}|{now}|{expires}"
    sig = _sign(body, secret)
    raw = f"{body}|{sig}"
    return base64.urlsafe_b64encode(raw.encode("utf-8")).decode("ascii").rstrip("=")


def verify_token(
    token: str,
    secret: str,
    *,
    now: int | None = None,
) -> TokenPayload | None:
    """Return the decoded payload if token is valid AND unexpired, else None."""
    if not token or not secret:
        return None
    try:
        padded = token + "=" * (-len(token) % 4)
        raw = base64.urlsafe_b64decode(padded.encode("ascii")).decode("utf-8")
    except Exception:
        return None
    parts = raw.split("|")
    if len(parts) != 5:
        return None
    email, niche, issued_str, expires_str, sig = parts
    body = "|".join(parts[:4])
    expected_sig = _sign(body, secret)
    if not hmac.compare_digest(sig, expected_sig):
        return None
    try:
        issued_at = int(issued_str)
        expires_at = int(expires_str)
    except ValueError:
        return None
    if now is None:
        now = int(time.time())
    if now > expires_at:
        return None
    return TokenPayload(
        email=email, niche=niche,
        issued_at=issued_at, expires_at=expires_at,
    )
