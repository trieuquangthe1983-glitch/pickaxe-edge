"""AI-engineering vertical-pack curated content — the EVERGREEN layer.

Highest-WTP audience: AI/ML engineers earn $200k+, the field moves so fast
they actually need quarterly content playbooks, and most maintain personal
blogs / Twitter. Same authoring framework as crypto_trading_pack.

Topics calibrated to Q2 2026: agentic frameworks, MCP, evals, prompt
caching cost optimization, RAG vs long-context, distillation.
"""

from __future__ import annotations

from core.vertical_pack import NicheContent


AI_ENGINEERING_CONTENT = NicheContent(
    niche="ai_engineering",
    title="AI Engineering Content Arbitrage Pack",
    subtitle=(
        "Where the AI eng audience is asking but nobody's writing yet. "
        "For builders shipping agents, evals, and infra who want their writing "
        "to compound instead of disappearing into the LinkedIn AI-slop ocean."
    ),

    platform_hooks={
        "youtube": (
            "Live-code an [agent / eval harness / RAG pipeline] in 20 minutes — narrate the trade-offs as they come up.",
            "'I switched from [popular framework] to [alternative] for production. Here's the latency + cost diff with real numbers.'",
            "The [N]-minute teardown: why [popular library]'s default config is wrong for [common use case].",
            "Build a benchmark in front of the camera comparing [model A] vs [model B] on YOUR data, not the leaderboards.",
        ),
        "tiktok": (
            "0-3s: show the prompt-cache hit rate going from 12% to 89%. 4-60s: explain the one config change.",
            "'I cut my OpenAI bill 70%. Here's the one Cursor trick they don't want you to know.' (with the actual API screenshot).",
            "Live-screen-record an agent doing something genuinely surprising in 45 seconds. No narration until second 30.",
            "60-second framework: 'Eval-driven dev in 4 questions' with a screenshare of an actual eval running.",
        ),
        "twitter": (
            "Show your prompt-cache hit rate before and after the change. Two screenshots, one tweet, no commentary needed.",
            "Counter-take on a viral AI tweet: 'X is wrong because [specific benchmark / specific case], here's the test you can run yourself.'",
            "The cost-per-task table: same task, 5 model+prompt configurations, dollars per 1k calls. Save and share fodder.",
            "Quote-RT a model release with: 'Ran [specific eval] in 10 min. Score: X. Compare to [prior model]: Y. Notable because Z.'",
        ),
        "linkedin": (
            "The CTO post: 'Our team migrated from [X] to [Y]. Here's the architecture diff and the 6-week timeline. (Plus the parts that broke.)'",
            "What the latest model release means for the build-vs-buy decision your team faces this quarter — 4 specific scenarios.",
            "Risk-management lens: how we evaluate AI vendors after [recent failure]. 5-point framework non-AI execs can apply.",
            "The eval/observability story most teams skip: why we built our own harness and what we'd reuse if starting today.",
        ),
        "reddit": (
            "'I tried [popular framework] for [task] and it failed in this specific way. Here's my repro and what I learned.'",
            "Genuine question: how are you handling [specific edge case in agents/RAG]? Here's my approach, here's where it breaks.",
            "Detailed write-up of [specific pipeline] with the prompt files, the eval scores, and the cost breakdown. AMA.",
            "Counter-thread on [popular argument]: I think the consensus is wrong because [specific evidence + reproducible test].",
        ),
        "substack": (
            "'The eval I wish I'd run before shipping [project]'. With the prompt files, the data, and the methodology.",
            "Deep dive on [architectural decision]: the 3 options, what we tried, what we shipped, what we'd do differently.",
            "Why prompt caching changes everything (with the math): a $X to $Y cost-per-MAU breakdown.",
            "The [N]-framework I use for [agent / RAG / fine-tune decision]. Includes the spreadsheet.",
        ),
    },

    platform_anti_hooks={
        "youtube": (
            "Faceless 'top 10 AI tools' videos — saturated by AI-spam channels, kills credibility.",
            "Reaction videos to OpenAI/Anthropic announcements without independent testing — adds zero value.",
            "Thumbnails with a shocked face + 'X IS DEAD' — works for hustle channels, kills technical audience trust.",
        ),
        "tiktok": (
            "Static slide-deck videos with AI voiceover — the audience can smell it immediately.",
            "ChatGPT prompt screenshots without the OUTPUT or the use case — feels like content theft from Twitter.",
            "'AI will replace [job]' fear-mongering without evidence — looks lazy on TikTok, where attention is earned in 3 seconds.",
        ),
        "twitter": (
            "Engagement-bait threads with no code, no numbers, no benchmark — devs flag these instantly.",
            "Hype tweets about new models without independent testing — credibility-destroying when next release supersedes.",
            "Listicles ('10 prompts to make you 10x'') — works on grifters' Twitter, fails with builders.",
        ),
        "linkedin": (
            "Reposts of OpenAI/Anthropic blog posts with 'Game changer!' — algorithm penalizes shallow engagement.",
            "AI-generated thought-leadership posts (the audience can tell) — torches trust within a single post.",
            "'AGI is here' speculation — reads as gambling content; LinkedIn's algorithm and your prospects both demote you.",
            "Generic 'AI will transform [industry]' takes — saturated since 2023, no signal value.",
        ),
        "reddit": (
            "Self-promotion in r/MachineLearning or r/LocalLLaMA without months of substantive contribution first — instant ban.",
            "Title-only posts asking 'what's the best LLM for X?' — auto-removed; the question has been answered 100 times.",
            "Posting benchmarks without methodology — gets eviscerated by the community.",
        ),
        "substack": (
            "AI-generated longform with no original benchmarks or code — paywall-resistant readers will not return.",
            "Listicles of papers without commentary — Hacker News covers this for free, faster.",
            "No 'I was wrong about X' content — without honest mistakes, retention dies in 2-3 issues.",
        ),
    },

    format_adaptations={
        ("long_video", "short_video"): (
            "Find the moment of highest 'wait, did that just work?' tension (the agent doing something surprising, "
            "the cache hit rate jumping). Put it in the first 3 seconds. One claim, one visual, one CTA. 30-60s."
        ),
        ("long_video", "thread"): (
            "Extract the 1-sentence thesis from the video. Build a 7-10 tweet thread: claim -> 3 evidence tweets "
            "(with screenshots of eval/cost numbers) -> 2 counter-arguments addressed -> conclusion. Link the video at the END."
        ),
        ("long_video", "post"): (
            "Strip framework-specific jargon. Lead with the business impact (cost saved / latency cut / risk avoided). "
            "Add the architecture diff in a single bullet list. End with a question for CTOs. 1000-1400 chars."
        ),
        ("thread", "longform_text"): (
            "Each tweet becomes a paragraph + an explanation of the WHY. Add the actual prompt files and eval JSON "
            "as gists/embeds. Write a proper conclusion section. Footnote section linking to original sources."
        ),
        ("thread", "post"): (
            "Strip developer jargon (kv-cache, MoE, RoPE). Add one paragraph of business context. "
            "Convert your spiciest claim into a question at the end to invite CTO/PM replies. 1200-1500 chars."
        ),
        ("thread", "short_video"): (
            "Take the SINGLE most counterintuitive claim from the thread. Open the video with that claim verbalized. "
            "Show the screenshot from the thread as the supporting visual. Use the rest of the thread as the script."
        ),
        ("longform_text", "thread"): (
            "Extract every numeric finding (cost, latency, eval score, hit rate). Each becomes its own tweet. "
            "Lead the thread with the most contrarian number, not the conclusion. Save the conclusion for the LAST tweet."
        ),
        ("longform_text", "long_video"): (
            "Use the essay as the script. Live-screen the eval running for everything that's a number. "
            "Speed-narrate sections without code; slow down on every code/config snippet. Add chapter markers."
        ),
        ("discussion", "thread"): (
            "Take your top-upvoted reply. That's the thread thesis. Other comments in the discussion become "
            "supporting tweets. Credit the original Reddit post + thank specific commenters by reddit handle."
        ),
        ("discussion", "longform_text"): (
            "The original Reddit post becomes the introduction. Your reply chain becomes the body. "
            "Add a 'what I would change in my answer' section — this is the trust differentiator vs LinkedIn AI slop."
        ),
    },

    hot_topics=(
        "prompt-cache cost optimization with real $/MAU numbers (validated Twitter + Substack, gap on LinkedIn + TikTok)",
        "eval-driven agent development with reproducible harnesses (validated Substack + Twitter, gap on YouTube long-form)",
        "RAG vs long-context tradeoffs with cost/quality benchmarks (validated Twitter + YouTube, gap on LinkedIn)",
        "MCP server ecosystem teardowns and best practices (emerging, low supply across all platforms)",
        "AI agent observability and failure-mode logging frameworks",
        "batch API cost optimization patterns for high-volume workloads",
        "distillation patterns: when to fine-tune vs prompt-engineer vs both",
    ),

    dead_topics=(
        "'ChatGPT vs Claude' generic comparisons — saturated by content farms with zero independent testing",
        "'10 AI tools you must use' listicles — pure AI-spam territory; readers actively distrust",
        "'AGI is here' / 'AGI is far' philosophical speculation — no signal value, no retention",
        "'AI will replace [job]' fear-mongering — saturated and reputationally damaging",
        "Surface-level reactions to OpenAI / Anthropic releases without testing — DevRel teams cover this better",
        "Generic 'how to use ChatGPT' tutorials — covered exhaustively since 2023",
    ),

    emerging_topics=(
        "MCP server design patterns and security models (huge demand, almost no creators have shipped depth here)",
        "On-device inference cost economics — when Apple Silicon / NPUs beat API calls",
        "Multi-agent orchestration failure modes (loops, contradictions, cost explosions)",
        "AI eval-as-a-product patterns (selling evaluation harnesses to teams)",
        "Cross-vendor abstraction trade-offs: LiteLLM-style routers in production",
        "Synthetic data generation pipelines for niche domains (medical, legal, scientific)",
    ),

    edge_audit_questions=(
        "Can a stranger identify your work from 3 random posts without seeing your handle?",
        "Do you have a signature framework, naming convention, or methodology you use repeatedly?",
        "Can your most loyal reader explain your core thesis on AI engineering in one sentence?",
        "Have you publicly admitted a wrong technical bet (model choice, framework, architecture) in the last 90 days?",
        "Do you write about ONE narrow area of AI (e.g. evals, agents, RAG infra) and not 'AI' broadly?",
        "Is your vocabulary distinct from the consensus (you avoid: paradigm shift, game changer, revolutionary)?",
        "Can you publish a benchmark post in under 4 hours from idea to share?",
        "Do at least 50% of your posts include code, numbers, or reproducible benchmarks?",
        "Have you challenged a prominent figure's technical claim publicly in the last 90 days?",
        "Are at least 3 of your top-10 posts about the SAME sub-niche?",
        "Do you have a 'wall of work' (pinned thread, about page) showing your eval / cost / architecture wins?",
        "Have you turned down sponsorship from an AI vendor on principle in the last 12 months?",
        "Do you respond to technical replies (not just like them) within 24 hours of posting?",
        "Have you published a failed experiment in full detail this year?",
        "Are at least 25% of your followers also building or shipping in AI (not just observers)?",
        "Has another AI engineer cited your benchmark, framework, or post by name in the last 90 days?",
        "Do you publish on a fixed cadence (weekly substack, daily twitter, biweekly youtube)?",
        "Is your bio specific (mentions a sub-niche / stack / company size), not generic ('AI/ML engineer')?",
        "Do you have a written 'how I would falsify my main thesis' on your blog or pinned thread?",
        "Can you name 3 specific engineers (not influencers) whose work has changed your approach this year?",
    ),

    failure_modes=(
        "AI moves faster than your refresh cycle. Quarterly is the absolute minimum cadence; monthly is better. "
        "If a new flagship model drops mid-pack, the 'cost optimization' opportunities may need re-pricing in days, not weeks.",
        "LinkedIn AI engineering content is dominated by VPs and CTOs posting from corporate accounts. Individual "
        "engineers with anon handles will UNDER-perform on LinkedIn compared to the opportunities suggest. Open a real-name account.",
        "TikTok arbitrage is real for AI eng but requires actual screen recording skill. Animated slide decks with "
        "AI voiceover will be rejected by both the algorithm and the audience. Budget time for production.",
        "Twitter arbitrage closes fastest in AI eng — the audience is concentrated and signals propagate in hours, "
        "not weeks. Execute Twitter opportunities within 7 days or skip them.",
        "Reddit (r/LocalLLaMA, r/MachineLearning) requires a substantive comment history before posting works. "
        "If your account has fewer than 50 quality comments in the niche, build that first (4-6 weeks).",
        "This pack assumes your benchmarks are honest. Posting fake or cherry-picked benchmark numbers will be "
        "caught within 48 hours by the AI engineering audience and permanently damages your account. Don't.",
    ),

    deep_dive_template_by_target={
        "twitter": {
            "structure": (
                "Tweet 1: Lead with the single counterintuitive number from the source platform.",
                "Tweet 2-3: The methodology — how to reproduce the number in under 30 minutes.",
                "Tweet 4: Address the obvious objection (sample size, model version, prompt brittleness).",
                "Tweet 5: One screenshot showing the actual eval / cost dashboard / benchmark output.",
                "Tweet 6: 'What would make me change my mind' — earns engineer trust, prompts technical replies.",
                "Tweet 7: Conclusion + a specific question targeting builders (not 'thoughts?').",
            ),
            "cta": "Quote-RT the original source (a paper, a blog post, a thread). Tag the author by handle.",
            "posting_time_utc": "Tue/Wed/Thu 15:00-18:00 UTC (US west coast morning + EU evening overlap)",
            "estimated_length": "7-10 tweet thread; total ~1800 chars; one inline chart",
        },
        "linkedin": {
            "structure": (
                "Line 1: A specific cost / latency / quality number from your team's experience.",
                "Para 1: Restate with the business context (team size, scale, deadline).",
                "Para 2: The decision framework — readable to non-technical execs.",
                "Para 3: The specific implication for the reader's roadmap or budget.",
                "Para 4: A 1-sentence question targeting CTOs / Heads of Engineering.",
            ),
            "cta": "Tag specific industry peers (not influencers) by name for response, max 2.",
            "posting_time_utc": "Tue/Wed 09:00 + 17:00 UTC (US morning + EU close)",
            "estimated_length": "1000-1500 chars; one architecture diagram if relevant",
        },
        "tiktok": {
            "structure": (
                "0-3s: The screen-record moment of surprise (cache hit jump, agent doing something).",
                "3-15s: State the claim verbally + show the supporting screenshot.",
                "15-45s: The proof point — one specific number, one specific config change.",
                "45-60s: The implication + CTA ('follow for the part-2 breakdown' or 'comment your use case').",
            ),
            "cta": "'Follow for the part-2 breakdown' OR 'Comment your stack and I'll respond with the closest match'",
            "posting_time_utc": "Daily 17:00-20:00 local (whatever your primary audience timezone is)",
            "estimated_length": "30-60 seconds, vertical 9:16, screen-record dominant",
        },
        "substack": {
            "structure": (
                "Hook (1 paragraph): the most counterintuitive number from the source platform with full context.",
                "Body (5-8 sections): each section is one claim + benchmark + reproducible methodology.",
                "Code exhibit (gist embed) + cost table.",
                "'What I tried that did not work' section — non-negotiable for technical trust.",
                "Conclusion (1 paragraph) + subscribe CTA + link to spreadsheet/repo.",
            ),
            "cta": "Subscribe CTA at top + bottom; share button after the strongest benchmark; repo link at the end.",
            "posting_time_utc": "Sunday 14:00 UTC OR Tuesday 14:00 UTC (Sunday for retention, Tuesday for share velocity)",
            "estimated_length": "1500-3000 words; code blocks and tables count toward perceived depth",
        },
        "youtube": {
            "structure": (
                "0-10s: The hook + the specific outcome ('cut cost 70%' / 'agent solved this in 3 turns').",
                "10-60s: Set up the context — what failed before, what you're testing.",
                "1-12min: Live-screen the eval running, the config change, the cost dashboard.",
                "12-15min: The decision framework — when this applies, when it doesn't.",
                "Last 30s: CTA, plus tease of the next experiment.",
            ),
            "cta": "Pinned comment with the repo / config / prompt files; ask viewers to share their hit-rate in replies.",
            "posting_time_utc": "Thursday 18:00 UTC (peak weekly retention for technical content)",
            "estimated_length": "10-20 min longform; tighter is fine if the demo warrants",
        },
        "reddit": {
            "structure": (
                "Title: A specific, falsifiable benchmark claim — not clickbait.",
                "TL;DR (3 lines max, includes the headline number).",
                "Methodology section (with code links).",
                "Results section (tables, not screenshots — Reddit prefers raw markdown).",
                "Sources section (papers, repos, prior threads).",
                "'Where this might be wrong' section.",
                "Genuine question at the end.",
            ),
            "cta": "Respond to every top-level comment within 12 hours — algorithm reward + community trust.",
            "posting_time_utc": "Sunday/Monday 14:00 UTC (lowest moderator activity, highest weekly retention)",
            "estimated_length": "800-2500 words; benchmarks need depth",
        },
    },
)
