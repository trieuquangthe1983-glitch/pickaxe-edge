"""Crypto-trading vertical-pack curated content — the EVERGREEN layer.

This is the high-trust portion of the $99 product. Authored, not generated.
Buyer pays not for the algorithm but for these specific, opinionated takes.

If/when topics or platform dynamics shift materially, edit this file and
re-package. That's the quarterly refresh cycle.
"""

from __future__ import annotations

from core.vertical_pack import NicheContent


CRYPTO_TRADING_CONTENT = NicheContent(
    niche="crypto_trading",
    title="Crypto Trading Content Arbitrage Pack",
    subtitle=(
        "Where demand has been validated, where supply is empty, and the exact "
        "hooks that work platform-by-platform. For traders and creators who "
        "want to skip the trend chase."
    ),

    platform_hooks={
        "youtube": (
            "Walk through the chart of [event] with one specific claim, then explain why everyone else got it wrong.",
            "'I was wrong about [coin/event]. Here's what I missed and what I'm doing now.'",
            "The [N]-minute explainer on [obscure mechanism], with a paid example that paid off / failed.",
            "Tear apart [popular influencer]'s recent trade thesis with on-chain or order-book evidence.",
        ),
        "tiktok": (
            "Open with the moment of highest tension — chart click, alert sound, 'wait...'.",
            "'POV: you held [coin] through [event]' + a real P&L screenshot in second 3.",
            "60 seconds: 'Three liquidation signals you missed last week' + show them on the chart.",
            "'I just did this trade. Watch what happens.' — paper trade or small size, narrate the move.",
        ),
        "twitter": (
            "The [funding rate / OI / liquidations / basis] is screaming X. Here's why nobody is saying it:",
            "Quick thread: what just happened in the last 4 hours nobody is talking about.",
            "If you held [coin] through [date], here is the actual P&L (not the meme).",
            "Three things from [conference / event / report] that nobody is reporting on:",
        ),
        "linkedin": (
            "The structural story behind [event]: regulatory, institutional, and market-microstructure angles.",
            "What [Fortune 500 / TradFi institution] just did with crypto, and what it means for your portfolio strategy.",
            "Risk management lesson from [recent failure] — applies whether you trade crypto or not.",
            "Why we're seeing [trend] in crypto markets: a 3-bullet framework for the non-crypto-native.",
        ),
        "reddit": (
            "Genuine question: how are you all handling [specific edge case]? Here is what I've tried, here is what I'm stuck on.",
            "I have been quiet for [period]. Here is the trade journal, including the losses.",
            "Detailed breakdown of [mechanic] for people who keep asking — with the math.",
            "Counter-take on [popular thread]: I think the consensus is wrong because [evidence].",
        ),
        "substack": (
            "Why I'm long/short [thesis] — and the specific things that would prove me wrong.",
            "The [N]-step framework I use for [strategy]. Includes the spreadsheet.",
            "What [recent event] actually means for derivatives markets (with the math).",
            "I've been quiet for [period]. Here's the trade journal — wins, losses, and what I'd do differently.",
        ),
    },

    platform_anti_hooks={
        "youtube": (
            "Thumbnails with shocked face + red arrow + dollar signs — works for grift, kills trust with serious traders.",
            "'Top 10 altcoins for 2026' listicles — saturated to oblivion.",
            "Price predictions without timeframe and without your position size — pure noise.",
        ),
        "tiktok": (
            "TradFi-style charts with no narration — audience cannot follow.",
            "Long monologues without a moment of tension in the first 3 seconds — algorithm kills you.",
            "Crypto slang ('wagmi/lfg/ngmi') without context — works for in-group but kills new-viewer conversion.",
        ),
        "twitter": (
            "Hot takes without on-chain or order-book evidence — replies will eat you.",
            "Vague predictions ('big move coming') — credibility-destroying when you're wrong.",
            "Engagement-bait questions ('what coin are you holding?') — algorithmically rewarded, brand-destroying.",
        ),
        "linkedin": (
            "Crypto slang of any kind — reads as childish on a corporate platform.",
            "Memes without thesis — algorithm punishes pure entertainment posts here.",
            "'Wen moon' / 'few understand' tone — kills professional referrals stone dead.",
            "Direct price predictions — reads as gambling content; LinkedIn deprioritizes.",
        ),
        "reddit": (
            "Self-promotion in r/CryptoCurrency or r/Bitcoin without 10:1 community contribution first — instant ban.",
            "Title-only posts with no body — auto-removed in most quality subs.",
            "Repeating consensus arguments — won't get upvoted; you need a real counter-take or genuine question.",
        ),
        "substack": (
            "Vague macro essays without specific trades or positions — readers can get this from Bloomberg for free.",
            "Listicles ('5 reasons BTC will moon') — paywall-resistant readers expect depth.",
            "No 'I was wrong about X' content — without intellectual honesty, retention dies.",
        ),
    },

    format_adaptations={
        ("long_video", "short_video"): (
            "Find the single highest-tension moment (chart click, 'wait...', P&L reveal). "
            "Put it in the first 3 seconds. Use 1 idea, 1 visual, 1 CTA. 30-60s max."
        ),
        ("long_video", "thread"): (
            "Extract the core thesis as a 1-sentence claim. Build a 7-10 tweet thread: "
            "claim -> 3 evidence tweets -> 2 counter-arguments addressed -> conclusion. "
            "Embed 1-2 chart screenshots, link to the full video at the end (not the start)."
        ),
        ("long_video", "post"): (
            "Strip ALL slang. Lead with the conclusion. Add the regulatory/institutional context. "
            "End with a question that prompts a professional discussion. 800-1200 chars."
        ),
        ("thread", "longform_text"): (
            "Each tweet becomes a paragraph. Add 1-2 chart embeds. Write a proper conclusion section. "
            "Add a footnote section linking to original sources (X profiles, on-chain data, papers)."
        ),
        ("thread", "post"): (
            "Strip crypto-specific jargon (wagmi, ngmi, alpha). Add ONE paragraph "
            "of business context. Convert your thesis into a question at the end "
            "to invite comments. 1200-1500 chars sweet spot."
        ),
        ("thread", "short_video"): (
            "Take the SINGLE most counterintuitive claim from the thread. Open the video "
            "with that claim as a hook. Use the rest of the thread as the script structure."
        ),
        ("longform_text", "thread"): (
            "Extract every data point that fits in 280 chars as its own tweet. "
            "Lead the thread with the most controversial claim, not the conclusion. "
            "Save the conclusion for the LAST tweet — drives saves."
        ),
        ("longform_text", "long_video"): (
            "Use the essay as the script outline. Add live chart annotations for "
            "anything that involves prices or order book. Speed-read sections that don't "
            "need visuals; slow down where the chart matters."
        ),
        ("discussion", "thread"): (
            "Take your top reply (the one that got upvoted most). That's the thread thesis. "
            "Other comments in the thread become supporting tweets. Tag your sources from Reddit."
        ),
        ("discussion", "longform_text"): (
            "The original Reddit post becomes your introduction. Your accumulated replies "
            "become the body. Add the 'what would change my mind' section that Reddit comment "
            "threads usually lack."
        ),
    },

    hot_topics=(
        "funding rate arbitrage on perp DEXes (validated on Substack + Twitter, gap on LinkedIn)",
        "BTC spot ETF flow analysis (validated on YouTube + Twitter, gap on TikTok)",
        "perp basis decay mechanics (validated on Substack, near-zero supply on LinkedIn + TikTok)",
        "exchange counterparty risk frameworks (validated on Reddit + Twitter, low on TikTok)",
        "60-sec liquidation cascade explainers (validated on TikTok, zero on LinkedIn)",
        "stablecoin yield arbitrage post-MakerDAO restructuring",
        "settlement-skew signals around futures expiry",
    ),

    dead_topics=(
        "'BTC to $100k' price predictions — every creator already has one",
        "Generic DCA-into-BTC advice — saturated since 2017",
        "'Top 10 altcoins for 2026' listicles — impossible to stand out, AI-spam infested",
        "'Why fiat is dying' rants — echo-chamber content, won't grow new audience",
        "Exchange-X-vs-Y fee comparisons — low-trust niche, looks like affiliate spam",
        "'What is Bitcoin' explainers — content saturation index near 100%",
    ),

    emerging_topics=(
        "L2 fee economics and how settlement margins compress for sequencers",
        "Real-world-asset tokenization regulatory analysis by jurisdiction",
        "AI-agent trading frameworks (intersection of crypto + agentic AI)",
        "Tax-loss-harvesting in crypto across multi-jurisdiction portfolios",
        "Post-quantum cryptography migration plans for major chains (3-5 year horizon)",
        "Restaking risk concentration and slashing-cascade modeling",
    ),

    edge_audit_questions=(
        "Can a stranger identify your work from 3 random posts without your handle showing?",
        "Do you have a signature phrase, framework, or metric you use repeatedly?",
        "Can your most loyal follower explain your trading thesis in one sentence?",
        "Have you publicly admitted a wrong trade or analysis in the last 90 days?",
        "Do you write about ONE niche within crypto (e.g. perps), not 'crypto' broadly?",
        "Is your vocabulary distinct from the consensus (you avoid: moon, wagmi, gm, ngmi)?",
        "Can you produce a chart-based piece in under 30 minutes from idea to publish?",
        "Do at least 30% of your posts include numbers, math, or specific trades?",
        "Have you said something unpopular about a prominent figure in the last 90 days?",
        "Are at least 3 of your top-10 posts about the SAME sub-niche?",
        "Do you have a 'wall of work' (pinned thread, about page) explaining your edge?",
        "Have you turned down a sponsor/affiliate offer in the last 12 months on principle?",
        "Do you re-engage with your replies (not just like) within 24h of posting?",
        "Have you documented at least one losing trade with full P&L this year?",
        "Do at least 20% of your followers also follow each other (cohesion)?",
        "Have you been quoted/cited by another creator in the last 90 days?",
        "Do you publish on a fixed cadence (weekly Substack, daily Twitter, etc.)?",
        "Is your bio specific (mentions a strategy/timeframe), not generic ('trader, investor')?",
        "Do you have a written 'what would change my mind' on your main thesis?",
        "Can you name 3 specific people whose work has changed your mind this year?",
    ),

    failure_modes=(
        "Arbitrage closes fast. Every report you act on, you also signal — assume your gap "
        "narrows within 30-60 days. Pay for the quarterly refresh OR re-run the tool yourself.",
        "Crypto cycles overrule everything. In a hot bull, 'BTC to $100k' content beats every "
        "arbitrage opportunity in this pack on raw engagement. The pack optimizes for DEFENSIBILITY, "
        "not peak engagement.",
        "LinkedIn arbitrage is real but requires a non-anon professional brand. If your handle is "
        "'@cryptochad42' you will NOT capture LinkedIn opportunities here. Open a separate professional account.",
        "Substack arbitrage rewards depth (1500+ words minimum). If you can't write that long, "
        "skip the Substack opportunities and double down on Twitter/Reddit ones.",
        "Format adaptation difficulty is REAL effort, not RISK. A topic with low difficulty might still "
        "take 4-6 hours to produce well. Budget time accordingly.",
        "This pack assumes you have an existing audience (>2k followers somewhere). If you're at "
        "zero, the arbitrage analysis matters less than just SHIPPING — fix the volume problem first.",
    ),

    deep_dive_template_by_target={
        "twitter": {
            "structure": (
                "Tweet 1: Open with the most counterintuitive claim from the source platform.",
                "Tweet 2-3: Lay out the 2-3 pieces of evidence.",
                "Tweet 4: Address the obvious counter-argument head-on.",
                "Tweet 5: One specific chart or screenshot.",
                "Tweet 6: 'What would change my mind' — earns trust, prompts replies.",
                "Tweet 7: Conclusion + a question that invites a counterpoint (not generic engagement-bait).",
            ),
            "cta": "Quote-RT the post that originally inspired the thread; credit the source platform.",
            "posting_time_utc": "Tue/Wed/Thu 13:00-15:00 UTC (US market open + EU end-of-day overlap)",
            "estimated_length": "7-10 tweet thread; total ~1800 chars across",
        },
        "linkedin": {
            "structure": (
                "Line 1: A specific number or claim (not 'in this post we'll...').",
                "Para 1: Restate the claim with 1 piece of context.",
                "Para 2: The mechanism / framework — keep it accessible to non-crypto readers.",
                "Para 3: Specific implication for the reader's business or portfolio.",
                "Para 4: A 1-sentence question that invites professional comments.",
            ),
            "cta": "End with a question targeting CFOs/risk managers, not retail traders.",
            "posting_time_utc": "Tue/Wed 09:00 + 17:00 UTC (US morning + EU close)",
            "estimated_length": "1000-1400 chars; long enough to expand, short enough to scan",
        },
        "tiktok": {
            "structure": (
                "0-3s: The hook moment (chart click, alert, P&L reveal).",
                "3-15s: State the claim verbally in 1 sentence + show the supporting visual.",
                "15-45s: The proof point — one specific example, one number.",
                "45-60s: The implication + the CTA.",
            ),
            "cta": "'Follow for the part-2 breakdown' OR 'Comment your timeframe and I'll do a custom one'",
            "posting_time_utc": "Daily 18:00-21:00 local (whatever your primary audience timezone is)",
            "estimated_length": "30-60 seconds, vertical 9:16",
        },
        "substack": {
            "structure": (
                "Hook (1 paragraph): the most counterintuitive thing from the source platform.",
                "Body (5-8 sections): each section is one claim + evidence + counter-argument.",
                "Spreadsheet / data exhibit (optional but recommended).",
                "'What would change my mind' section — non-negotiable for trust.",
                "Conclusion (1 paragraph) + CTA to subscribe / share.",
            ),
            "cta": "Subscribe CTA at the top AND bottom; share button mid-post (after the strongest claim).",
            "posting_time_utc": "Sunday 14:00 UTC (start-of-week reading; highest open rate)",
            "estimated_length": "1500-2500 words; longer if you have a spreadsheet exhibit",
        },
        "youtube": {
            "structure": (
                "0-10s: The hook + the specific outcome of the video.",
                "10-60s: Set up the context with chart annotations.",
                "1-5min: Walk through the analysis step-by-step.",
                "5-8min: The specific trade idea or framework — explicit and reproducible.",
                "Last 30s: CTA, plus tease of next video.",
            ),
            "cta": "Pinned comment with the spreadsheet/sources; ask viewers to share their P&L in replies.",
            "posting_time_utc": "Thursday 19:00 UTC (peak weekly retention window)",
            "estimated_length": "8-15 minute longform; tighter is fine if the analysis warrants",
        },
        "reddit": {
            "structure": (
                "Title: A specific, falsifiable claim — not clickbait.",
                "TL;DR (3 lines max).",
                "The full analysis (markdown formatting, headers, lists).",
                "Sources section (links to on-chain data, papers, prior threads).",
                "'Where I might be wrong' section.",
                "Genuine question to the community at the end.",
            ),
            "cta": "Respond to every top-level comment within 12 hours — drives the algorithm.",
            "posting_time_utc": "Sunday/Monday 14:00 UTC (slowest moderation, highest retention)",
            "estimated_length": "800-2000 words; depth matters more than length",
        },
    },
)
