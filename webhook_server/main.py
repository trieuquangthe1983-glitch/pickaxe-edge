"""FastAPI server for Gumroad webhook handling.

Run locally:
    pip install -r requirements-webhook.txt
    $env:GUMROAD_WEBHOOK_SECRET = "..."
    $env:PACK_REFRESH_SECRET    = "..."
    uvicorn webhook_server.main:app --reload --port 8000

Deploy paths (see docs/DEPLOY.md):
- Render (recommended for paid plan): one-click web service
- Fly.io: `fly launch && fly deploy`
- Cloudflare Workers (free): rewrite in JS — out of scope here
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

# Make project root importable when launched via `uvicorn webhook_server.main:app`
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from fastapi import FastAPI, Query, Request
from fastapi.responses import JSONResponse

from core.webhook import handle_gumroad_ping
from webhook_server.email_provider import get_sender_from_env


app = FastAPI(
    title="PICKAXE-EDGE Gumroad Webhook",
    description="Receives Gumroad Ping notifications, issues refresh tokens, emails buyer.",
    version="0.1.0",
)


@app.get("/")
def root() -> dict:
    return {
        "service": "pickaxe-edge-webhook",
        "ok": True,
        "endpoints": {"health": "/health", "gumroad_ping": "POST /webhooks/gumroad?key=SECRET"},
    }


@app.get("/health")
def health() -> dict:
    pack_ok = bool(os.environ.get("PACK_REFRESH_SECRET"))
    hook_ok = bool(os.environ.get("GUMROAD_WEBHOOK_SECRET"))
    return {
        "ok": pack_ok and hook_ok,
        "pack_refresh_secret_set": pack_ok,
        "gumroad_webhook_secret_set": hook_ok,
        "email_provider": os.environ.get("EMAIL_PROVIDER", "console"),
    }


@app.post("/webhooks/gumroad")
async def gumroad_ping(
    request: Request,
    key: str = Query("", description="Shared webhook secret"),
) -> JSONResponse:
    # Gumroad sends form-encoded payload
    form = await request.form()
    payload = {k: v for k, v in form.items()}

    result = handle_gumroad_ping(
        payload,
        shared_secret=os.environ.get("GUMROAD_WEBHOOK_SECRET", ""),
        submitted_secret=key,
        pack_secret=os.environ.get("PACK_REFRESH_SECRET", ""),
        expected_seller_id=os.environ.get("GUMROAD_SELLER_ID") or None,
        email_sender=get_sender_from_env(),
        app_url=os.environ.get("APP_URL", "https://YOUR-APP.streamlit.app"),
        token_valid_days=int(os.environ.get("TOKEN_VALID_DAYS", "90")),
    )

    body = {
        "ok": result.ok,
        "reason": result.reason,
        "email": result.email,
        "niche": result.niche,
        # Do NOT echo the token in the response — Gumroad logs every webhook
        # response body, and tokens are bearer credentials. Email is the only
        # channel a token should ever leave this server through.
    }
    # Return 200 even on logical rejection so Gumroad doesn't retry forever;
    # but return 500 for real internal errors (missing secrets).
    status = 200 if result.ok else (
        500 if "not configured" in result.reason else 200
    )
    return JSONResponse(body, status_code=status)
