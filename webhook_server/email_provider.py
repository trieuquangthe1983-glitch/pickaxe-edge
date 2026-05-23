"""Pluggable email providers for webhook token delivery.

Two providers shipped:
- console: prints to stdout, useful for local development
- resend:  Resend.com transactional API (100/day free tier)

Set EMAIL_PROVIDER=resend in env to enable real email. Requires
RESEND_API_KEY and RESEND_FROM_EMAIL also set.

Adding a new provider (Postmark, Mailgun, SES) = subclass and register here.
"""

from __future__ import annotations

import json
import os
import sys
import urllib.request
from typing import Callable

EmailSender = Callable[[str, str, str], None]


def console_sender(to: str, subject: str, body: str) -> None:
    """Print the email to stdout. Useful for local dev / dry-run."""
    print("\n" + "=" * 70, flush=True)
    print(f"[EMAIL] To: {to}", flush=True)
    print(f"        Subject: {subject}", flush=True)
    print("-" * 70, flush=True)
    print(body, flush=True)
    print("=" * 70 + "\n", flush=True)


def resend_sender(api_key: str, from_email: str) -> EmailSender:
    """Return a sender that posts to https://api.resend.com/emails."""
    if not api_key:
        raise ValueError("resend_sender requires api_key")
    if not from_email or "@" not in from_email:
        raise ValueError("resend_sender requires from_email")

    def _send(to: str, subject: str, body: str) -> None:
        req = urllib.request.Request(
            "https://api.resend.com/emails",
            method="POST",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "User-Agent": "pickaxe-edge-webhook/0.1",
            },
            data=json.dumps({
                "from": from_email,
                "to": [to],
                "subject": subject,
                "text": body,
            }).encode("utf-8"),
        )
        with urllib.request.urlopen(req, timeout=15) as resp:
            if resp.status >= 300:
                raise RuntimeError(f"Resend API returned HTTP {resp.status}")

    return _send


def get_sender_from_env() -> EmailSender:
    """Pick the configured provider from env, fall back to console with warning."""
    provider = os.environ.get("EMAIL_PROVIDER", "console").lower()

    if provider == "resend":
        api_key = os.environ.get("RESEND_API_KEY", "").strip()
        from_email = os.environ.get("RESEND_FROM_EMAIL", "").strip()
        if not api_key or not from_email:
            print(
                "WARNING: EMAIL_PROVIDER=resend but RESEND_API_KEY / "
                "RESEND_FROM_EMAIL not set. Falling back to console sender.",
                file=sys.stderr,
            )
            return console_sender
        return resend_sender(api_key, from_email)

    if provider != "console":
        print(
            f"WARNING: unknown EMAIL_PROVIDER={provider!r}, using console.",
            file=sys.stderr,
        )

    return console_sender
