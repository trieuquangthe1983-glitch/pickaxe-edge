"""CLI to issue pack refresh tokens. Run after a Gumroad/Stripe sale notification.

Usage:
    # First time on your machine:
    $env:PACK_REFRESH_SECRET = "your-long-random-secret-here"

    # Each sale:
    python scripts/issue_token.py buyer@example.com crypto_trading
    python scripts/issue_token.py buyer@example.com ai_engineering --days 90

Paste the printed token into the customer's email or Gumroad receipt.
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

# Make project root importable when run as a script
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from core.refresh_token import generate_token  # noqa: E402


SUPPORTED_NICHES = ("crypto_trading", "ai_engineering")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Issue a $49 pack-refresh token for a buyer.",
    )
    parser.add_argument("email", help="Buyer email address")
    parser.add_argument(
        "niche", choices=SUPPORTED_NICHES,
        help="Which vertical pack they purchased",
    )
    parser.add_argument(
        "--days", type=int, default=90,
        help="Token validity in days (default: 90 = one quarter)",
    )
    parser.add_argument(
        "--app-url", default="https://YOUR-APP.streamlit.app",
        help="Your deployed app URL for the refresh delivery message",
    )
    args = parser.parse_args(argv)

    secret = os.environ.get("PACK_REFRESH_SECRET", "").strip()
    if not secret:
        print("ERROR: PACK_REFRESH_SECRET env var not set.", file=sys.stderr)
        print("Set it with a long random string (e.g. `python -c \"import secrets; print(secrets.token_urlsafe(32))\"`)",
              file=sys.stderr)
        return 1

    try:
        token = generate_token(
            args.email, args.niche, secret, valid_days=args.days,
        )
    except ValueError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1

    print()
    print("=" * 70)
    print(f"  Token issued for {args.email}")
    print(f"  Niche: {args.niche}  ·  Valid: {args.days} days")
    print("=" * 70)
    print()
    print(token)
    print()
    print("---  Paste this block into the Gumroad receipt / customer email  ---")
    print()
    print(f"Your refresh access:")
    print(f"  URL:   {args.app_url}/Pack_Refresh")
    print(f"  Token: {token}")
    print()
    print(f"This token is valid for {args.days} days. Re-purchase any time after for a fresh snapshot.")
    print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
