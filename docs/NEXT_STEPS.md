# Next steps — push to GitHub + deploy to Streamlit Cloud

Local repo is ready: branch `main`, 1 commit, 45 files, no secrets included.

## Step 1: Create empty GitHub repo (2 min)

1. Go to https://github.com/new
2. Repository name: `pickaxe-edge`
3. Visibility: **Public** (required for Streamlit Community Cloud free tier;
   for private, you'd need the $20/mo Streamlit Teams plan)
4. **Do NOT** check "Add a README" / "Add .gitignore" / "Add license" —
   repo must be empty so local repo can become the source of truth
5. Click "Create repository"
6. Copy the URL shown (looks like `https://github.com/YOUR_USERNAME/pickaxe-edge.git`)

## Step 2: Push from local (1 min)

```powershell
cd C:\Users\Administrator\pickaxe-edge
# Replace YOUR_USERNAME with your actual GitHub handle
git remote add origin https://github.com/YOUR_USERNAME/pickaxe-edge.git
git push -u origin main
```

If GitHub asks for auth, use a Personal Access Token, not password (passwords
disabled since 2021). Generate one at https://github.com/settings/tokens with
the `repo` scope.

## Step 3: Deploy to Streamlit Cloud (5 min)

1. Visit https://share.streamlit.io and sign in with GitHub
2. Click "New app"
3. Repository: `YOUR_USERNAME/pickaxe-edge`
4. Branch: `main`
5. Main file path: `ui/app.py`
6. Click "Deploy"

First build takes ~3 minutes (installs `streamlit`, `pandas`, `pytest`).
You'll get a URL like `https://YOUR_USERNAME-pickaxe-edge-ui-app-xyz.streamlit.app`.

## Step 4: Add YouTube API key as secret (2 min, optional — only if you got a key)

1. In Streamlit Cloud dashboard, open your app
2. Click the three dots -> "Settings" -> "Secrets"
3. Paste:
```toml
YOUTUBE_API_KEY = "AIzaSy...your-key-here"
```
4. Click "Save". App auto-restarts. "Use live YouTube" toggle becomes enabled.

## Step 5: Sanity check the live URL

Visit your `https://...streamlit.app` URL. Check that:
- All 5 tabs load: Niche scan / Arbitrage / Edge audit / Quote builder / Client report
- Sidebar shows the 3 live-data toggles (YouTube disabled if no key configured)
- Tab 5 generates a Markdown report and the download button works

If the app fails to boot, click "Manage app" in Streamlit Cloud dashboard ->
view logs. Most common issue: a dependency in `requirements.txt` is too new
for Streamlit Cloud's Python version. Pin to known-good versions if needed.

## Step 6: First outreach (use the live URL!)

The first DM you send should reference YOUR LIVE APP. Modified script 1 from
`docs/OUTREACH/dm-scripts-en.md`:

> Hey {first_name} — built a tool that finds content topics validated on
> one platform but absent from another. Free audit (~5 min): tell me your
> niche, I'll send a report. Tool runs here if you want to poke at it:
> {YOUR_STREAMLIT_URL}

The live URL acts as proof — they can see the tool exists, see the niche
options, see what a report looks like. Far stronger than just "I built a thing."

## Costs after deploy

| Item | Cost |
| --- | --- |
| Streamlit Cloud free tier | $0 |
| GitHub public repo | $0 |
| YouTube API (10k units/day free) | $0 unless you exceed quota |
| Reddit JSON API (unauthenticated) | $0 |
| Substack RSS | $0 |
| **Total to launch** | **$0** |

When you hit paying clients (week 2-3), consider upgrading from Streamlit
Cloud to Render ($7/mo) for always-on (no cold-start delay on prospect
clicks). See `docs/DEPLOY.md` Option B.
