"""Indie SaaS vertical-pack curated content.

Target audience: solo + small-team SaaS founders, PMs, and content marketers
who already follow Lenny Rachitsky, Tomasz Tunguz, Kyle Poyar, April Dunford.
This audience is content-marketing-aware (most have written blog posts) and
explicitly pays for newsletters — predictably converts to a $99 product.

Voice: data-driven, framework-heavy, low jargon. Avoid 'founder hustle' tone.
"""

from __future__ import annotations

from core.vertical_pack import NicheContent


INDIE_SAAS_CONTENT = NicheContent(
    niche="indie_saas",
    title="Indie SaaS Content Arbitrage Pack",
    subtitle=(
        "Where your prospective customers are reading but your competitors "
        "aren't writing. For founders, PMs, and B2B content marketers tired "
        "of fighting 50 other newsletters for the same VP-of-Eng's attention."
    ),

    platform_hooks={
        "youtube": (
            "Live-screenshare your pricing page experiment + the conversion numbers, before and after.",
            "Walk through a real cohort retention chart from your product — explain the inflection points.",
            "Build a [free trial / freemium / reverse trial] decision tree on a whiteboard in 12 minutes, with 1 case study each.",
            "Live teardown of [competitor / acquired startup]'s funnel with a stopwatch + dollar estimates.",
        ),
        "tiktok": (
            "0-3s: 'We doubled trial conversion by removing ONE checkbox.' Show the before/after screenshot in second 4.",
            "60-second framework: 'How to spot bad pricing in 30 seconds' with 3 examples on screen.",
            "'I cold-emailed 100 CTOs. Here's what worked. (Screenshare 3 winning emails.)'",
            "Live-record yourself reading a Lenny survey result + your contrarian take in under 60s.",
        ),
        "twitter": (
            "Your pricing page A/B test result with both screenshots. One tweet. Save fodder.",
            "Quote-tweet a [Lenny / Tunguz] post: 'Disagree because [specific data from my product]. Here's what happened when we tried it.'",
            "The cold-outbound cohort table: 100 prospects, broken by reply rate, meeting rate, close rate, with the actual numbers.",
            "Daily build-in-public update with the specific metric that moved (not 'made progress' — the number).",
        ),
        "linkedin": (
            "The CRO/CMO post: 'We moved from [pricing model] to [new model]. 90-day result: $X ARR delta. Here's the playbook.'",
            "What [recent SaaS acquisition / shutdown] teaches us about [market positioning / TAM thinking]. 4-bullet framework.",
            "The board-meeting post: 'What our investors asked vs. what we wish they'd asked' — distill to 5 questions.",
            "Cross-functional teardown: how [pricing / churn / GTM] decisions ripple through eng+CS+marketing — with the org chart.",
        ),
        "reddit": (
            "Detailed write-up of [pricing experiment] including the hypothesis, the variants, the result, and what we'd do differently.",
            "Genuine question: how do you handle [specific edge case in PLG/sales-led]? Here's my approach, here's where it breaks.",
            "Counter-take on [popular SaaS thread]: 'I think the consensus is wrong because [specific data], here's the cohort I'd want to see'.",
            "Show-and-tell with the actual product: '6 months in, here's our ARR / churn / LTV — AMA on the playbook'.",
        ),
        "substack": (
            "The [N]-step framework I use for [pricing / GTM / onboarding] decisions. Includes the spreadsheet template.",
            "Why I'm betting against [popular SaaS thesis] — with the specific things that would prove me wrong.",
            "Cohort deep-dive on [retention / expansion]: the chart, the bucket definitions, the action items per bucket.",
            "I've been quiet for [period]. Here's the strategy doc that came out of it — annotated with what's working.",
        ),
    },

    platform_anti_hooks={
        "youtube": (
            "Generic 'how to build a SaaS' tutorials — saturated since 2015, kills credibility with operators.",
            "Talking-head 'thought leader' interviews with no data on screen — audience swipes away.",
            "Thumbnails with 'I built a $1M SaaS in 90 days' — works for hustle channels, kills B2B trust.",
        ),
        "tiktok": (
            "AI-voiced 'top 10 SaaS tools' slideshows — algorithm and audience both reject.",
            "Founder selfie videos with no data, no demo, no specifics — saturated with bad content.",
            "Crypto-style 'this WILL change everything' tone — your B2B prospects will block you.",
        ),
        "twitter": (
            "Engagement-bait threads with no numbers, no cohort data, no benchmark — eaten alive by the SaaS community.",
            "Vague 'just shipped' posts without the metric — looks lazy when your competitors share specific numbers.",
            "Listicles of 'X tools every founder should use' — pure affiliate spam optics.",
        ),
        "linkedin": (
            "Reposts of TechCrunch articles with 'Game changer!' — algorithm penalizes shallow engagement.",
            "AI-generated thought-leadership posts — VPs of Sales can spot these instantly; trust torched in one post.",
            "Founder fluff: 'grateful for the journey' / 'humbled by the team' — works for IPO posts, kills B2B content.",
            "'10 lessons from my 10x exit' — saturated and increasingly satirized.",
        ),
        "reddit": (
            "Self-promotion on r/SaaS or r/Entrepreneur without months of substantive contribution — instant ban.",
            "Generic 'what's your favorite tool' questions — auto-removed; answered 1000 times.",
            "Show-and-tell without metrics — gets ignored; the community wants data.",
        ),
        "substack": (
            "Vague macro essays on 'the future of SaaS' — paywall-resistant readers want operational specifics.",
            "Listicles or 'X lessons from [famous founder]' — Lenny does this better; you cannot compete on volume.",
            "No 'here's what we tried that failed' content — without honest mistakes, retention dies in 3 issues.",
        ),
    },

    format_adaptations={
        ("long_video", "short_video"): (
            "Find the single screenshot moment — the cohort chart, the pricing experiment result, the dashboard. "
            "Lead with it in second 0. One claim, one number, one CTA. 30-60s."
        ),
        ("long_video", "thread"): (
            "Pull the 1-sentence thesis from the video. Build a 7-10 tweet thread: claim -> 3 evidence tweets "
            "(with chart screenshots + specific numbers) -> 2 counter-arguments -> conclusion. Link the video LAST."
        ),
        ("long_video", "post"): (
            "Strip startup jargon. Lead with the business outcome ($ delta / % delta in specific metric). "
            "Add the framework in 3-5 bullets. End with a question targeting your buyer persona. 1000-1400 chars."
        ),
        ("thread", "longform_text"): (
            "Each tweet expands into a paragraph + a 'why this works' explanation. Add the underlying spreadsheet "
            "or cohort definition. Write a proper conclusion. Footnote section linking to sources."
        ),
        ("thread", "post"): (
            "Strip Twitter shorthand (DMs, QTs, RT). Add one paragraph of B2B context. "
            "Convert the spiciest claim into a question for senior leaders. 1200-1500 chars."
        ),
        ("thread", "short_video"): (
            "Take the SINGLE highest-engagement tweet from the thread. Open the video with that claim verbalized. "
            "Show the thread screenshot as the supporting visual."
        ),
        ("longform_text", "thread"): (
            "Extract every number (cohort %, pricing delta, conversion rate). Each becomes its own tweet. "
            "Lead the thread with the most contrarian number, not the conclusion. Save the framework for the LAST tweet."
        ),
        ("longform_text", "long_video"): (
            "Use the essay as the script. Live-screen the dashboard/spreadsheet for every number cited. "
            "Speed-narrate sections without data; slow down on every chart or experiment screenshot."
        ),
        ("discussion", "thread"): (
            "Take your top-upvoted reply from the Reddit/Indie Hackers thread. That's the Twitter thesis. "
            "Other comments become supporting tweets. Credit the original post + thank specific commenters."
        ),
        ("discussion", "longform_text"): (
            "Original community post becomes the introduction. Your reply chain becomes the body. "
            "Add a 'what I would change in my answer' section — the trust differentiator vs LinkedIn slop."
        ),
    },

    hot_topics=(
        "pricing-page conversion experiments with before/after numbers (validated Twitter + LinkedIn, gap on YouTube)",
        "cold outbound to enterprise tactics with reply-rate cohort data (validated LinkedIn + Twitter, gap on YouTube)",
        "free trial vs freemium vs reverse trial frameworks (validated Substack + Twitter, gap on Reddit)",
        "shipping in public weekly with the specific moved metric (validated Twitter + LinkedIn, gap on Substack longform)",
        "expansion revenue / NDR mechanics with cohort breakdown",
        "AI tool integration impact on SaaS cost structure and pricing",
        "PLG -> sales-assist transition playbooks (real timelines, not theory)",
    ),

    dead_topics=(
        "'10 lessons from my exit' — saturated and increasingly satirized",
        "Generic 'how to validate your SaaS idea' — covered exhaustively since 2015",
        "'No-code is the future' takes — boring at this point; audience has moved on",
        "'Why bootstrapping > VC' (or vice versa) without specific evidence — pure tribalism",
        "Affiliate-bait 'best CRM/email/analytics tool' listicles — pure spam optics",
        "Founder selfie 'grateful for the journey' posts — IPO-day exception only",
    ),

    emerging_topics=(
        "AI-assisted SDR workflows and how they reshape MEDDIC / sales cycles",
        "Usage-based pricing math for AI-powered features (cost-of-goods-sold concerns)",
        "Cross-platform analytics for SaaS post-Cookieless (server-side, attribution chains)",
        "Customer-led growth: when CS teams own pipeline (vs marketing)",
        "Founder-mode operating systems — beyond the Paul Graham essay, real playbooks",
        "Compliance-as-a-product: SOC2, ISO27001 as growth lever (not a tax)",
    ),

    edge_audit_questions=(
        "Can a stranger identify your work from 3 random posts without seeing your handle?",
        "Do you have a signature framework, metric, or methodology you use repeatedly?",
        "Can your most loyal reader explain your core thesis in one sentence?",
        "Have you publicly admitted a wrong strategic bet (pricing, GTM, hire) in the last 90 days?",
        "Do you write about ONE specific area of SaaS (e.g. PLG, enterprise sales, B2B SEO) and not 'startups' broadly?",
        "Is your vocabulary distinct from the consensus (you avoid: synergy, leverage, journey, hustle)?",
        "Can you publish a cohort-data post in under 4 hours from idea to share?",
        "Do at least 50% of your posts include real numbers from your own product (not borrowed benchmarks)?",
        "Have you publicly challenged a Lenny / Tunguz / Andreessen post in the last 90 days with a counter-argument?",
        "Are at least 3 of your top-10 posts about the SAME sub-niche of SaaS?",
        "Do you have a 'wall of work' (pinned thread, about page) showing your specific operating wins?",
        "Have you turned down a sponsorship or paid placement in the last 12 months on principle?",
        "Do you respond to substantive replies (not just like them) within 24 hours of posting?",
        "Have you published a failed experiment in full detail this year (hypothesis + result + lesson)?",
        "Are at least 25% of your followers also operating / building in B2B SaaS (not just observers)?",
        "Has a peer SaaS operator (not influencer) cited your post or framework by name in the last 90 days?",
        "Do you publish on a fixed cadence (weekly Substack, daily Twitter, monthly long-form)?",
        "Is your bio specific (mentions ARR band, stage, role-type), not generic ('founder, builder')?",
        "Do you have a written 'how I would falsify my main thesis' on your blog or pinned thread?",
        "Can you name 3 specific operators (not investors, not influencers) whose work has changed your approach this year?",
    ),

    failure_modes=(
        "SaaS cycles have a 6-9 month attention rhythm. Opportunities in 'pricing experiments' may be saturated "
        "by Q3 if you delay. Execute within 30 days or skip.",
        "LinkedIn rewards executives, not solo founders. If your title is 'co-founder, 3-person team', LinkedIn "
        "engagement will under-perform what this pack suggests. Either build up to 1k followers first OR co-publish "
        "with someone with a VP title at a larger company.",
        "Twitter SaaS arbitrage closes fastest of all niches — the audience is concentrated (~50k accounts), signals "
        "propagate in hours. Twitter opportunities have a 7-day execution window or skip.",
        "Substack arbitrage in SaaS requires you to be objectively as good or better than Lenny / Tunguz / Poyar "
        "on the SAME topic — they cover everything already. Pick a sub-niche they DON'T (e.g. SOC2-as-growth, "
        "founder-mode-for-engineers) where you have real depth.",
        "Reddit (r/SaaS, r/Entrepreneur) has near-zero trust for new accounts. Spend 4-6 weeks substantively "
        "commenting before posting. The arbitrage signal is real but requires audience-trust capital.",
        "This pack assumes you have a product with real data to cite (cohorts, MRR, conversion). If you're pre-launch, "
        "the deep-dive opportunities won't work — your posts will have 'borrowed' numbers and the audience can tell. "
        "Build product first, then use this pack.",
    ),

    deep_dive_template_by_target={
        "twitter": {
            "structure": (
                "Tweet 1: Lead with the most counterintuitive number from your own product (or source post).",
                "Tweet 2-3: The methodology — how to reproduce the experiment in 2 weeks.",
                "Tweet 4: Address the obvious objection (sample size, segment specificity, survivorship bias).",
                "Tweet 5: One screenshot of the actual cohort/dashboard/pricing page.",
                "Tweet 6: 'What would make me change my mind' — trust-building, prompts senior replies.",
                "Tweet 7: Conclusion + specific question targeting your buyer persona (not 'thoughts?').",
            ),
            "cta": "Quote-RT the original source (Lenny survey, Tunguz post, internal data). Tag the author by handle.",
            "posting_time_utc": "Tue/Wed/Thu 13:00-15:00 UTC (US morning + EU end-of-day)",
            "estimated_length": "7-10 tweet thread; total ~1800 chars; one inline chart screenshot",
        },
        "linkedin": {
            "structure": (
                "Line 1: A specific cost / ARR / conversion number from your product or research.",
                "Para 1: Restate with business context (segment, team size, deadline).",
                "Para 2: The decision framework — written for VPs and Heads of, not founders only.",
                "Para 3: The specific implication for the reader's roadmap or budget cycle.",
                "Para 4: A 1-sentence question targeting CRO/CMO/Head of Product.",
            ),
            "cta": "Tag specific industry peers (operators, not influencers) by name for response; max 2.",
            "posting_time_utc": "Tue/Wed 09:00 + 17:00 UTC (US morning + EU close)",
            "estimated_length": "1000-1500 chars; one architecture/cohort diagram if relevant",
        },
        "tiktok": {
            "structure": (
                "0-3s: The screen-record moment (dashboard, pricing page, cohort chart).",
                "3-15s: State the claim verbally + show the supporting screenshot.",
                "15-45s: The proof point — one specific number, one specific change you made.",
                "45-60s: The implication + CTA (follow for part 2 or comment your stage).",
            ),
            "cta": "'Follow for the part-2 breakdown' OR 'Comment your ARR band and I'll send the closest case study'",
            "posting_time_utc": "Daily 17:00-20:00 local timezone of your primary audience",
            "estimated_length": "30-60 seconds, vertical 9:16, screen-record dominant",
        },
        "substack": {
            "structure": (
                "Hook (1 paragraph): the most counterintuitive number with full context.",
                "Body (5-8 sections): each section is one claim + cohort + reproducible methodology.",
                "Spreadsheet / dashboard exhibit (embedded screenshot + Google Sheets link).",
                "'What I tried that did not work' section — non-negotiable for B2B trust.",
                "Conclusion (1 paragraph) + subscribe CTA + link to template / spreadsheet.",
            ),
            "cta": "Subscribe CTA at top + bottom; share button after the strongest cohort chart.",
            "posting_time_utc": "Sunday 14:00 UTC OR Tuesday 14:00 UTC (Sunday retention, Tuesday velocity)",
            "estimated_length": "1500-3000 words; data tables and screenshots count toward perceived depth",
        },
        "youtube": {
            "structure": (
                "0-10s: The hook + specific outcome ('doubled trial conversion' / 'cut CAC 40%').",
                "10-60s: Context — what was failing, what you're testing.",
                "1-12min: Live-screen the dashboard, the experiment dashboard, the pricing page.",
                "12-15min: The decision framework — when this applies, when it doesn't.",
                "Last 30s: CTA, plus tease of next experiment.",
            ),
            "cta": "Pinned comment with the spreadsheet template; ask viewers to share their numbers in replies.",
            "posting_time_utc": "Thursday 18:00 UTC (peak weekly retention for B2B content)",
            "estimated_length": "10-20 min longform; tighter is fine if the dashboard tells the story",
        },
        "reddit": {
            "structure": (
                "Title: A specific, falsifiable result — not clickbait.",
                "TL;DR (3 lines max, includes the headline number).",
                "Methodology section (segment, time period, what you measured).",
                "Results section (tables in markdown, not screenshots).",
                "Sources section (links to Lenny survey, Tunguz post, internal docs).",
                "'Where this might be wrong' section.",
                "Genuine question at the end (not 'thoughts?').",
            ),
            "cta": "Respond to every top-level comment within 12 hours — algorithm + community trust.",
            "posting_time_utc": "Sunday/Monday 14:00 UTC (lowest moderation, highest weekly retention)",
            "estimated_length": "800-2500 words; cohort + framework depth matters",
        },
    },
)
