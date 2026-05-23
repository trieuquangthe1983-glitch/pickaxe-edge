# Next steps — full launch walkthrough

Your chosen path: **Streamlit Cloud (free) + Render webhook ($7/mo) + Resend
email (free tier) + Gumroad slugs configured post-deploy.**

Total time to live URL: ~45 minutes. Total ongoing cost: ~$7/mo.

Local repo state: 5 commits on `main` branch, 143 tests passing, no remote.

---

## Phase 1: Generate your secrets (one-time, 2 min)

You need 2 long random strings. Generate them now and save somewhere
safe (1Password, a text file you keep offline). You'll paste them into
multiple places below.

```powershell
# Run twice, save each output as PACK_REFRESH_SECRET and GUMROAD_WEBHOOK_SECRET
python -c "import secrets; print(secrets.token_urlsafe(48))"
python -c "import secrets; print(secrets.token_urlsafe(48))"
```

Set them locally so you can also issue tokens via CLI as backup:

```powershell
# Open your PowerShell profile (creates if missing)
if (-not (Test-Path $PROFILE)) { New-Item -Path $PROFILE -ItemType File -Force }
notepad $PROFILE

# Add these two lines, save, restart PowerShell:
$env:PACK_REFRESH_SECRET      = "the-first-secret-you-generated"
$env:GUMROAD_WEBHOOK_SECRET   = "the-second-secret-you-generated"
```

---

## Phase 2: GitHub repo + push (5 min)

```powershell
# 1) Create empty repo at https://github.com/new
#    Name: pickaxe-edge
#    Visibility: PUBLIC (Streamlit Cloud free tier requires public)
#    DO NOT initialize with README

# 2) Push your local repo (replace YOUR_USERNAME)
cd C:\Users\Administrator\pickaxe-edge
git remote add origin https://github.com/YOUR_USERNAME/pickaxe-edge.git
git push -u origin main

# If GitHub asks for auth: use a Personal Access Token, not password
# Create one at https://github.com/settings/tokens with `repo` scope
```

---

## Phase 3: Deploy Streamlit Cloud (5 min)

1. Visit https://share.streamlit.io and sign in with GitHub
2. Click "New app"
3. Settings:
   - Repository: `YOUR_USERNAME/pickaxe-edge`
   - Branch: `main`
   - Main file path: `ui/app.py`
4. Click "Deploy". First build takes ~3 minutes.
5. Note your URL — something like `https://YOUR_USERNAME-pickaxe-edge-ui-app-xyz.streamlit.app`

### Configure Streamlit secrets (so refresh + dashboard pages work)

1. In Streamlit Cloud dashboard, open your app
2. Three-dot menu -> Settings -> Secrets
3. Paste this TOML (replace placeholder):

```toml
PACK_REFRESH_SECRET = "the-first-secret-you-generated"
# Optional, if you got a YouTube API key earlier:
# YOUTUBE_API_KEY = "AIzaSy..."
```

4. Save. App auto-restarts.

### Sanity-check the Streamlit deploy

- Open the URL. All 5 tabs should load.
- Navigate to `/Pack_Refresh` (e.g. `https://your-url/Pack_Refresh`) — should
  show "Paste your refresh token" form, NOT the "not configured" error.
- Same for `/Buyer_Dashboard`.

---

## Phase 4: Set up Resend (free email, 10 min)

1. Sign up at https://resend.com (free)
2. Add your sending domain:
   - If you have one (e.g. yourdomain.com): Dashboard -> Domains -> Add Domain
   - Add the DNS records they show (SPF + DKIM + DMARC). Cloudflare/Namecheap
     interface takes ~3 minutes. Verification 5-15 minutes.
   - If you don't have a domain: use `onboarding@resend.dev` for testing
     (limited to 100/day TO YOUR OWN EMAIL, not customers). Get a domain.
3. Create API Key:
   - Dashboard -> API Keys -> Create API Key
   - Permission: "Sending access"
   - Copy the `re_...` key — you'll paste it into Render in Phase 5

---

## Phase 5: Deploy Render webhook ($7/mo, 15 min)

The webhook is a SEPARATE service from your Streamlit app. They live in the
same git repo but deploy independently.

### Create the service

1. Visit https://render.com and sign in with GitHub
2. Click "New +" -> "Web Service"
3. Connect your `pickaxe-edge` repo
4. Settings:
   - Name: `pickaxe-edge-webhook`
   - Region: pick the one closest to your customers
   - Branch: `main`
   - Runtime: **Python 3**
   - Build command: `pip install -r requirements-webhook.txt`
   - Start command: `uvicorn webhook_server.main:app --host 0.0.0.0 --port $PORT`
   - Plan: **Starter ($7/mo)** — needed for always-on; free tier sleeps

### Set environment variables (Render dashboard -> Environment)

```
PACK_REFRESH_SECRET     = the-first-secret-you-generated   ← SAME as Streamlit
GUMROAD_WEBHOOK_SECRET  = the-second-secret-you-generated
APP_URL                 = https://YOUR-STREAMLIT-URL.streamlit.app
EMAIL_PROVIDER          = resend
RESEND_API_KEY          = re_xxxxxxxxxxxxxxxxxxxxxxxxx
RESEND_FROM_EMAIL       = packs@yourdomain.com   ← must be your verified domain
```

Optional (recommended):
```
GUMROAD_SELLER_ID       = your-gumroad-seller-id   ← see step below for finding it
TOKEN_VALID_DAYS        = 90
```

5. Click "Create Web Service". First deploy takes ~3 min.
6. Note your webhook URL — something like `https://pickaxe-edge-webhook.onrender.com`

### Verify webhook is alive

```powershell
# Replace with your real URL
curl https://pickaxe-edge-webhook.onrender.com/health
# Expected: {"ok":true, "pack_refresh_secret_set":true, "gumroad_webhook_secret_set":true, ...}
```

If `ok: false`, check Render dashboard -> Logs for the missing env var.

---

## Phase 6: Create Gumroad listings + configure (10 min)

1. Sign up / log in to https://gumroad.com
2. Find your seller_id:
   - Dashboard -> Settings -> Profile -> URL shows `gumroad.com/SELLER_HANDLE`
   - The numeric seller_id appears in API responses; check Settings -> Advanced
3. Create 4 products (3 packs + 1 refresh):

| Product | Slug suggestion | Price | Delivery message |
|---|---|---|---|
| Crypto Trading Pack | `pickaxe-crypto` | $99 | (see below) |
| AI Engineering Pack | `pickaxe-ai-eng` | $99 | (see below) |
| Indie SaaS Pack | `pickaxe-saas` | $99 | (see below) |
| Pack Refresh (any niche) | `pickaxe-refresh` | $49 | (see below) |

For each product:
- Product type: "Digital product"
- Content: (skip — webhook delivers via email)
- Delivery message (in "Thank you" section):
  ```
  Thank you for your purchase!

  Your refresh token and download link will arrive in an email within
  1-2 minutes. Check spam if it doesn't appear.

  Token URL: https://YOUR-STREAMLIT-URL.streamlit.app/Pack_Refresh
  Dashboard:  https://YOUR-STREAMLIT-URL.streamlit.app/Buyer_Dashboard
  ```

### Hook up the webhook

1. Gumroad: Settings -> Advanced -> "Ping" / "Resource Subscriptions"
2. Set Ping URL to:
   ```
   https://pickaxe-edge-webhook.onrender.com/webhooks/gumroad?key=YOUR_GUMROAD_WEBHOOK_SECRET
   ```
   (substitute the SECOND secret you generated in Phase 1)
3. Save.

### Tell the webhook which Gumroad slugs map to which niches

If you used the EXACT default slugs (`pickaxe-crypto`, `pickaxe-ai-eng`,
`pickaxe-saas`), skip this — defaults work out of the box.

Otherwise, in Render dashboard -> your webhook service -> Environment, add:

```
PRODUCT_TO_NICHE_JSON = {"your-crypto-slug":"crypto_trading","your-ai-slug":"ai_engineering","your-saas-slug":"indie_saas"}
```

Render restarts the service. Verify via `/health`:

```powershell
curl https://pickaxe-edge-webhook.onrender.com/health
# Look for "product_to_niche": {...} with your custom mapping
# and "configured_via_env": true
```

---

## Phase 7: Test the full flow (10 min)

1. Make a $0 test purchase:
   - Gumroad lets you create discount codes. Make one for 100% off your
     Crypto pack, valid 1 use.
   - Buy your own product using the discount code, an email you can check.
2. Within 1-2 min: email arrives in your inbox with the refresh token.
3. Visit your Streamlit `/Pack_Refresh`. Paste the token. Click verify.
4. Click "Generate fresh pack". Download. Open the Markdown — you should see
   ~3000 words of curated + live arbitrage content.
5. Visit `/Buyer_Dashboard`. Paste the SAME token. See entitlements display.

If any step fails, check:
- Render dashboard -> Logs (webhook errors)
- Resend dashboard -> Emails (delivery failures)
- Streamlit Cloud dashboard -> Logs (verification errors)

---

## Phase 8: First outreach (use the live URL!)

You now have proof artifacts to point at:

- **Free demo:** `https://your-streamlit.streamlit.app`
- **$99 product:** `https://gumroad.com/l/pickaxe-crypto`
- **$49 refresh:** `https://gumroad.com/l/pickaxe-refresh`

Modify outreach script #1 from `docs/OUTREACH/dm-scripts-en.md`:

> Hey {first_name} — I built a tool that finds content topics with proven
> demand on one platform but absent from another. Just shipped the
> {their-niche} version as a $99 self-serve pack. Want a free preview of
> what you'd get? Tool runs here: {YOUR_STREAMLIT_URL}

---

## Ongoing cost summary

| Item | Cost | When you pay |
|---|---|---|
| Streamlit Cloud free | $0 | Forever (unless you go paid for private apps) |
| GitHub public repo | $0 | Forever |
| Render webhook starter | $7/mo | Always on |
| Resend free tier | $0 | < 100 emails/day |
| Gumroad fee | 10% per sale | Per transaction |
| Reddit/Substack APIs | $0 | Forever |
| YouTube Data API | $0 | Below 10k units/day |
| **Total fixed** | **$7/mo** | |

Break-even: **1 pack sale every 14 days** covers the infra.

---

## Troubleshooting common issues

### "Token invalid" on Pack_Refresh
- `PACK_REFRESH_SECRET` must be IDENTICAL on Streamlit Cloud + Render webhook
  + your local PowerShell profile. Verify all three.

### Webhook returns 200 but no email arrives
- Resend domain not verified yet (15 min DNS propagation)
- Check Resend dashboard -> Emails -> look for the attempted send
- Email landed in customer's spam (add `packs@yourdomain.com` to your warm-up list)

### Gumroad webhook never fires
- Gumroad's Ping URL must include `?key=YOUR_GUMROAD_WEBHOOK_SECRET` — easy to forget
- Some Gumroad plans only ping on "Resource Subscriptions" not basic Ping; check your plan
- Test by triggering a $0 sale with discount code, then `tail` Render logs

### App URL shows "this app is sleeping"
- Streamlit Cloud free tier sleeps after inactivity (~30 min)
- First visit after sleep takes ~10s to wake — fine for prospect-driven traffic
- If hurting conversion, upgrade Render to $7/mo always-on Streamlit replacement
