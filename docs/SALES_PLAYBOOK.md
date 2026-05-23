# PICKAXE-EDGE — Sales Playbook

## The contrarian pitch (use this verbatim in cold outreach)

> Most creator tools tell you what's *trending* — which means by the time you
> use them, ten thousand other creators are making the same content. PICKAXE-EDGE
> does the opposite: it finds topics that have *already proven they work* on one
> platform but where nobody's serving them yet on another. Demand validated,
> competition empty. We sell you the map of those gaps.

## Who buys

In priority order — start where willingness-to-pay is highest:

1. **Solo creators with 10k-100k followers on ONE platform** wanting to expand.
   They've hit the ceiling of one channel and know they should diversify, but
   don't know where. Tier: **$500 audit**.
2. **Content agencies serving 5+ creator clients.** They need defensible IP
   beyond "we'll post for you." Tier: **$299/mo SaaS Agency** + flagship
   strategy projects.
3. **B2B SaaS founders doing content marketing.** They're hiring writers and
   getting generic LinkedIn posts. Show them where their competitors *aren't*.
   Tier: **$2,000 strategy** + **$299/mo retainer**.
4. **VC/PE portfolio companies in consumer/creator economy.** Portfolio-wide
   licence. Tier: **custom enterprise**.

## What NOT to do

- Don't position as "another analytics tool." That commodity market has
  Beehiiv, BuzzSumo, Hootsuite. They have free tiers. You lose.
- Don't bundle with content production. Your edge is *intelligence*, not labor.
  Stay sharp and high-margin.
- Don't sell to creators <10k followers. They lack the cash and the discipline
  to act on the data.

## First 30 days (validation, not scaling)

| Week | Goal | Action |
| --- | --- | --- |
| 1 | Ship the pack | Publish $99 Vertical Pack on Gumroad/Stripe; post about it on your main channel |
| 1 | 10 conversations | DM 30 mid-size creators offering FREE audit in exchange for feedback |
| 2 | 3 pack sales + 3 paid audits | First proof of WTP at low ticket + convert 3 free-audit recipients to $500 |
| 3 | 1 strategy | Upgrade the highest-engagement audit client to $2k strategy |
| 4 | 5 retainers | Pitch monthly briefing to all 10; close 5 at $299/mo |

If you hit week-4 numbers: $297 (3 packs) + $1,500 (audits) + $2,000 (strategy) +
$1,495 (retainers) = **$5,292 month 1**. Above breakeven from day 1. Validates demand.

If you DON'T hit it: the pitch is wrong, not the tool. Iterate on positioning
before building more features.

### Why the $99 pack first

- **Pack tests WTP at the lowest-friction price.** If nobody buys at $99,
  your $500 audit will not sell either — fix product or pitch BEFORE wasting
  outreach hours.
- **Pack is the ad for the audit.** Every buyer of the pack is a warm lead
  for the audit. Include a footer in the pack: "Want this customized for
  your handle? $500 audit." Pack -> audit conversion target: 10%.
- **Pack scales without your time.** Once it's on Gumroad, it sells while
  you sleep. Audits and retainers consume your hours.

## Pricing psychology

- **$500 audit** is the trojan horse. Cheap enough for impulse purchase,
  expensive enough that the client takes the report seriously. Never go below.
- **$2,000 strategy** is anchored by the $500 audit. Says "audit identifies, strategy
  executes." Use a 14-day delivery window — urgency pricing.
- **$299/mo retainer** is the LTV engine. One retainer = 7 months of an audit.
  Pitch as "stay ahead of platform shifts."
- **$49 SaaS** is the lead-gen layer, not the revenue layer. Don't sweat low
  conversion — its job is to make you findable.

## Asymmetric upsides (do not lead with these, but build for them)

- **White-label** for agencies → $299/mo unlocks unlimited client reports under
  their brand. Margin near 100%.
- **Vertical packs** — pre-built playbooks per niche (crypto trading shipped;
  add longevity / B2B SaaS / home automation / AI engineering / personal
  finance as content swaps using `core/vertical_pack.py`). Scales without
  your time. $99 each, $49 quarterly refresh, $299 5-niche bundle.
- **Affiliate** — pay creators 30% recurring for SaaS referrals AND 50%
  per pack sale (since pack margin is ~98%). They market because the product
  makes them look smart AND pays them.

## Vertical pack distribution

The crypto_trading pack ships first because the author has domain expertise.
Sequence for the next 4 packs (priority order):

1. **AI engineering** — fast-moving, creators desperate for differentiation,
   willingness-to-pay is highest. Same content authoring effort, larger TAM.
2. **Indie SaaS** — Lenny + Tom Tunguz audience, already pays for content
   newsletters; pack format is familiar.
3. **Longevity** — high-WTP audience (Peter Attia / Bryan Johnson followers),
   smaller TAM but premium pricing tolerance.
4. **Personal finance** — largest TAM but lowest per-buyer WTP; expect
   higher refund-attempt rate.
5. **Home automation** — niche; only do this if a prospect specifically
   asks. Low priority.

To author a new pack: copy `data/crypto_trading_pack.py` -> `data/<niche>_pack.py`,
edit content, register in `ui/app.py` `VERTICAL_PACKS` dict. The generator
handles everything else.

## Honest failure modes (tell prospects up front; builds trust)

1. **Platform data goes stale fast.** Re-run weekly minimum or you'll be
   recommending dead trends. Retainer is the answer.
2. **Arbitrage closes.** The moment you publish on the target platform, you're
   *signaling* the arbitrage. Take action quickly; don't sit on a report.
3. **Format adaptation is real work.** The tool finds the gap; *you* still have
   to make the content. Difficulty score sets expectations.
4. **Edge audit can be uncomfortable.** Some creators learn they have no edge.
   That's actionable too — be willing to deliver hard truths.

## One-line elevator (use everywhere)

> "We find the topics your audience already loves on YouTube but nobody's
> writing on LinkedIn yet. $500 to find them, $2000 to plan around them."
