# PICKAXE-EDGE

**Contrarian "pickaxe play" for the creator economy.**

Most creator tools chase trends — which means everyone makes the same content and margins collapse to zero. PICKAXE-EDGE does the opposite: it scans 6 platforms (YouTube, TikTok, Twitter/X, LinkedIn, Reddit, Substack) and finds **content arbitrage** — topics/formats that are validated as hot on Platform A but under-supplied on Platform B.

That's where the alpha lives: demand is already proven elsewhere, competition hasn't shown up yet.

## What it does

1. **Niche scan** — give a niche, it returns the top performers across all 6 platforms.
2. **Arbitrage finder** — cross-references each topic by platform, scores white-space opportunities.
3. **Edge audit** — for a creator, quantifies their actual differentiation (vocabulary uniqueness, audience cohesion, hook repeatability) so they stop producing undifferentiated slop.
4. **Pricing calculator** — turns the analysis into a productized service quote ($500 one-time audit / $2000 niche strategy / $299/mo retainer).
5. **Markdown report** — client-ready deliverable.

## Business model

This is itself a pickaxe play — sell the *output* to creators/agencies.

| Tier | Format | Price | Margin |
| --- | --- | --- | --- |
| **Vertical Pack** | **Self-serve Markdown download (1 niche)** | **$99** | **~98%** |
| Pack Refresh | Quarterly re-run of the same pack | $49 | ~98% |
| Audit | 1-time custom report (your handle) | $500 | ~95% |
| Strategy | 90-day plan + 2 revisions | $2,000 | ~90% |
| Retainer | Monthly briefing | $299/mo | ~92% |
| SaaS Pro | Self-serve, unlimited scans | $49/mo | ~85% |
| SaaS Agency | White-label, multi-client | $299/mo | ~88% |

See [docs/SALES_PLAYBOOK.md](docs/SALES_PLAYBOOK.md) for go-to-market.

## Run

```powershell
cd C:\Users\Administrator\pickaxe-edge
pip install -r requirements.txt
python -m pytest tests/ -v
streamlit run ui/app.py
```

## Architecture

- `core/` — engine (pure Python, no I/O, fully testable)
- `data/` — seed data simulating platform APIs (replace with real scrapers later)
- `ui/` — Streamlit dashboard
- `tests/` — pytest, deterministic
- `docs/` — sales + how-to-use

## Why mock data (for now)

Real platform APIs (TikTok, X, Reddit) have strict rate limits and TOS issues. The MVP ships with realistic seeded data across 6 niches so you can demo, sell, and validate willingness-to-pay BEFORE investing in scrapers. Real data sources slot into the same `PlatformSignal` interface in `data/sources.py`.
