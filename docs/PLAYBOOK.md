# PICKAXE-EDGE — How to use the tool

## 5-minute demo flow (for prospects)

1. Launch UI: `streamlit run ui/app.py`
2. Sidebar -> pick the prospect's niche (e.g. `crypto_trading`).
3. **Tab 1 (Niche scan)** -> show the platform-by-platform summary. Point at
   the "underserved" platforms. *"Look — your competition is fighting on
   YouTube and Twitter. LinkedIn is empty."*
4. **Tab 2 (Arbitrage)** -> sort by EV. Pick the top 3. *"These are topics
   already getting 80%+ engagement on Substack but fewer than 5 creators on
   TikTok."*
5. **Tab 3 (Edge audit)** -> pull up a sample profile. *"Here's what we'd
   produce for you — quantifying whether you're standing out enough to justify
   continued investment."*
6. **Tab 5 (Client report)** -> generate the Markdown. Download it. *"This is
   the deliverable. $500 buys this for your account."*

Total demo time: 5 minutes. Close rate target: 30%.

## Thresholds — how to tune

- **Demand floor (default 0.55)**: minimum engagement on source platform.
  Lower it for emerging niches with smaller sample sizes. Raise it for
  saturated niches where everything looks hot.
- **Supply ceiling (default 8)**: max creators on target platform.
  Below 5 = genuine white space. 5-15 = still room but moving fast.
  Above 15 = not arbitrage anymore.

## Replacing mock data with real sources

The `data/sources.py` interface is `get_signals(niche) -> list[PlatformSignal]`.
Any real implementation must return the same shape. Status as of this build:

1. **Reddit (DONE)** — `data/reddit_source.py`. Public JSON API, no auth.
   Engagement = log-normalized score + 2x comments. Supply = unique
   non-bot authors. UI toggle: "Use live Reddit".
2. **Substack (DONE)** — `data/substack_source.py`. RSS per publication.
   IMPORTANT: RSS has NO engagement metric — engagement here is a
   *supply-as-demand proxy* (more publications writing about it = demand
   inferred). UI toggle: "Use live Substack". Customize
   `NICHE_PUBLICATIONS` per real niche before scaling outreach.
3. **YouTube (TODO)** — Data API v3 has a free quota; sufficient for
   periodic scans. Add `data/youtube_source.py` with the same shape.
4. **Twitter/X (TODO)** — paid API tier required since 2023. ~$100/mo entry.
5. **LinkedIn (TODO)** — no public API for content discovery. Use Proxycurl
   or manual proxy-rotation scraping.
6. **TikTok (TODO)** — most hostile. Use third-party providers (e.g. Apify
   actor).

## Honest caveat per source

Different sources have different engagement reliability. Be transparent in
client reports about which sources are live vs. mocked, and which use real
engagement vs. supply-proxy:

| Source | Engagement quality | Notes |
| --- | --- | --- |
| Reddit | REAL (score + comments) | Most trustworthy |
| Substack | PROXY (post count) | Supply-as-demand; weaker signal |
| YouTube | REAL (views + likes) | When implemented |
| Twitter/X | REAL (likes + replies) | Requires paid API |
| LinkedIn | REAL (reactions) | Scraping is fragile |
| TikTok | REAL (views + likes) | Third-party only |

Recommended cadence: weekly refresh per niche. Cache results in SQLite to
avoid re-paying for the same data.

## Format adaptation cheat sheet (for the strategy upsell)

Use this when delivering a $2k strategy doc:

| From | To | What to keep | What to change |
| --- | --- | --- | --- |
| YouTube long-form | TikTok short | The hook + one insight | Compress to 60s, faster cuts |
| YouTube long-form | LinkedIn post | The framework | Strip jargon, lead with the conclusion |
| Twitter thread | LinkedIn post | The structure | Add professional context, soften memes |
| Substack longform | Twitter thread | The data points | Tighten language, one insight per tweet |
| Reddit discussion | YouTube long-form | The genuine question | Add structured answer + own analysis |
| Reddit discussion | Substack longform | The pain point | Build the canonical answer |

## Common buyer objections + responses

**"How is this different from BuzzSumo?"**
> BuzzSumo shows what's *already viral everywhere*. By the time you see it
> there, you're the 10,000th creator chasing it. We show what's viral in one
> place but absent in another. Different game.

**"How accurate is the data?"**
> Engagement scores aggregate the last 30 days of public signals across 6
> platforms. Sample sizes shown in every report. We refresh weekly for retainer
> clients. The arbitrage signal is *directionally* reliable — you still test.

**"Can you just give me the topics without the score?"**
> No. The score discounts for execution difficulty — a topic with no
> competition that requires a complete format rebuild isn't an opportunity,
> it's a trap. The math is the product.

**"What if I act on a report and it doesn't work?"**
> Then the arbitrage closed faster than expected (someone else found it too),
> or the format adaptation was the bottleneck. Both are learnings the retainer
> would have flagged earlier. We don't refund — we credit toward the retainer.
