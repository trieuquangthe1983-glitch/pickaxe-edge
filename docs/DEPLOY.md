# PICKAXE-EDGE — Deployment guide

Three deployment paths in order of effort. Pick one.

## Option A: Streamlit Community Cloud (recommended — FREE)

**Time:** 10 minutes. **Cost:** $0. **Limits:** 1 GB RAM, public-only, sleeps on inactivity.

### Steps

```powershell
# 1) Initialize git (one-time) — run from C:\Users\Administrator\pickaxe-edge
cd C:\Users\Administrator\pickaxe-edge
git init
git branch -M main
git add .
git commit -m "Initial PICKAXE-EDGE commit"

# 2) Create empty GitHub repo named 'pickaxe-edge' at:
#    https://github.com/new
#    Settings: PUBLIC (Streamlit Cloud free tier requires public)
#    Do NOT initialize with README — your local repo already has one.

# 3) Wire local to remote (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/pickaxe-edge.git
git push -u origin main

# 4) Visit https://share.streamlit.io
#    - "New app" -> pick the repo -> branch=main -> main file path = ui/app.py
#    - "Deploy". First build takes ~3 minutes.

# 5) You get a URL like: https://YOUR_USERNAME-pickaxe-edge-ui-app-xyz.streamlit.app
```

### Streamlit Cloud notes
- Uses `requirements.txt` (already pinned).
- Reads `.streamlit/config.toml` (already configured for headless).
- Free tier is fine for outreach demos (the app sleeps after inactivity and wakes in ~10s on the next visit — fine for prospect-driven traffic).

## Option B: Render.com (always-on, low cost)

**Time:** 15 minutes. **Cost:** $7/mo (Starter web service). **Limits:** None practical for this app.

### Steps

```powershell
# Reuse the same git repo from Option A.
# Visit https://render.com -> New + -> Web Service
#  - Connect GitHub repo
#  - Runtime: Python
#  - Build command: pip install -r requirements.txt
#  - Start command: streamlit run ui/app.py --server.port=$PORT --server.address=0.0.0.0
#  - Plan: Starter ($7/mo)
# The `Procfile` in repo is the fallback for buildpack-based deploys.
```

Render gives you a custom domain support and zero-downtime deploys on push. Use this when you have paying clients.

## Option C: Docker anywhere (Fly.io / Railway / your own VPS)

**Time:** 20-60 min depending on platform. **Cost:** $0-5/mo for hobby tiers.

The included `Dockerfile` is production-ready (slim image, healthcheck on `/_stcore/health`).

### Fly.io quickstart
```powershell
# Install flyctl from https://fly.io/docs/hands-on/install-flyctl/
fly launch --no-deploy        # follow prompts; pick app name pickaxe-edge
fly deploy
fly open
```

### Railway quickstart
```powershell
# Install Railway CLI: https://docs.railway.app/develop/cli
railway login
railway init
railway up
railway domain   # get public URL
```

### Local Docker (sanity test before remote deploy)
```powershell
docker build -t pickaxe-edge .
docker run -p 8501:8501 pickaxe-edge
# Open http://localhost:8501
```

## Pre-deploy checklist

Run this BEFORE pushing to any cloud:

```powershell
cd C:\Users\Administrator\pickaxe-edge
python -m pytest tests/ -q        # must show "49 passed" (or current count, 0 failed)
streamlit run ui/app.py            # boots without errors, all 5 tabs render
```

## Post-deploy: validate the live URL

```powershell
# Replace with your real URL
$URL = "https://your-app.streamlit.app"
Invoke-WebRequest "$URL/_stcore/health" -UseBasicParsing | Select-Object StatusCode
```

You should see `StatusCode: 200`.

## When to upgrade tier

| Symptom | Action |
| --- | --- |
| App sleeping is hurting prospects | Move from Streamlit Cloud (A) to Render (B) |
| Need custom domain (pickaxe-edge.com) | Render or Docker on Fly.io |
| Need private/auth-gated app | Streamlit Cloud Teams ($20/mo/user) or Render + simple auth proxy |
| Reddit rate-limited at scale | Add auth (Reddit OAuth: 100 req/min vs. 60 for anonymous) |

## Secrets

Do NOT commit API keys. Use the platform's secret store:
- **Streamlit Cloud:** App dashboard -> Settings -> Secrets, paste TOML content
- **Render:** Environment Variables tab in service settings
- **Fly.io:** `fly secrets set YOUTUBE_API_KEY=AIzaSy...`
- **Docker local:** `docker run -e YOUTUBE_API_KEY=AIzaSy... ...`

## YouTube API key setup (5 minutes)

The "Use live YouTube" toggle in the UI needs a `YOUTUBE_API_KEY`. Get one:

1. Open https://console.cloud.google.com and create a project (or reuse one)
2. APIs & Services -> Library -> search "YouTube Data API v3" -> Enable
3. APIs & Services -> Credentials -> "Create Credentials" -> "API Key"
4. Copy the key. Click "Restrict Key":
   - Application restrictions: HTTP referrers (for browser) or None for testing
   - API restrictions: select "YouTube Data API v3" only
5. Save.

### Local setup
```powershell
# Option A: env var (temporary, this PowerShell session only)
$env:YOUTUBE_API_KEY = "AIzaSy...your-key-here"
streamlit run ui/app.py

# Option B: secrets file (persistent, gitignored)
Copy-Item .streamlit/secrets.toml.example .streamlit/secrets.toml
# Edit .streamlit/secrets.toml and replace placeholder with real key
```

### Streamlit Cloud setup
1. Deploy the app (see Option A above)
2. App dashboard -> Settings -> Secrets
3. Paste this content (replace with real key):
```toml
YOUTUBE_API_KEY = "AIzaSy...your-key-here"
```
4. Save. App auto-restarts with the new secret.

### Quota budget

YouTube free tier = 10,000 units/day.
- Each topic search = ~150 units (1 search call + 1 batched video stats)
- 6 niches x ~4 topics each = 24 searches = ~3,600 units per full scan
- Budget for ~2-3 full scans per day; cached at TTL=3600 seconds in UI

Hitting quota returns `quotaExceeded` -> UI gracefully falls back to mock data
with a warning. Quota resets at midnight Pacific Time.

## Pack refresh secret setup

The `/Pack_Refresh` page (for paying buyers to re-generate their Vertical Pack)
needs `PACK_REFRESH_SECRET` set BOTH locally (to issue tokens via
`scripts/issue_token.py`) AND in the deployed environment (to verify tokens).

### Generate a strong secret (do this ONCE, save it)
```powershell
python -c "import secrets; print(secrets.token_urlsafe(48))"
```

### Set it locally (for issuing tokens after Gumroad sales)
```powershell
# Save in your PowerShell profile so it persists across sessions:
notepad $PROFILE
# Add this line, save:
$env:PACK_REFRESH_SECRET = "the-secret-you-just-generated"
```

### Set it on Streamlit Cloud (so the refresh page can verify)
1. App dashboard -> Settings -> Secrets
2. Add to the existing TOML content:
```toml
YOUTUBE_API_KEY = "AIzaSy..."
PACK_REFRESH_SECRET = "the-same-secret-you-just-generated"
```
3. Save. App restarts.

### Important: secret hygiene

- **The secret MUST be identical between your local machine and the deployed
  app** — otherwise tokens you issue won't verify.
- **Never commit the secret to git.** It belongs in `.streamlit/secrets.toml`
  (gitignored) locally, env var, or platform secret store.
- **Rotate the secret** if you suspect leak by:
  1. Generate a new secret
  2. Update Streamlit Cloud secrets AND your local env
  3. Re-issue tokens for all customers with active subscriptions
  Old tokens become invalid the moment you change the secret.

### Issuing tokens (after each Gumroad/Stripe sale)

```powershell
python scripts/issue_token.py buyer@example.com crypto_trading
# Copy the printed block into the Gumroad receipt / customer email
```
