"""Mock platform data. Replace with real scrapers later — same interface.

Realistic seeds for 6 niches across 6 platforms. The arbitrage opportunities
embedded in the data are intentional, so the engine can find them in tests.
"""

from __future__ import annotations

from core.types import PlatformSignal

NICHES = (
    "crypto_trading",
    "home_automation",
    "indie_saas",
    "longevity",
    "ai_engineering",
    "personal_finance",
)


# Format of each tuple: (platform, topic, engagement_0to1, supply_count_30d, sample_size)
_SEEDS: dict[str, list[tuple[str, str, float, int, int]]] = {
    "crypto_trading": [
        # CROSS-PLATFORM SAME TOPIC — shows arbitrage gaps
        ("youtube",  "funding rate arbitrage explained", 0.78, 12,  340),
        ("twitter",  "funding rate arbitrage explained", 0.82, 25,  890),
        ("tiktok",   "funding rate arbitrage explained", 0.30, 2,    18),  # low supply on TT
        ("linkedin", "funding rate arbitrage explained", 0.12, 1,     4),
        ("reddit",   "funding rate arbitrage explained", 0.65, 18,  120),
        ("substack", "funding rate arbitrage explained", 0.71,  6,   30),

        ("youtube",  "btc spot etf flow analysis",       0.85, 22,  600),
        ("twitter",  "btc spot etf flow analysis",       0.88, 45, 1200),
        ("tiktok",   "btc spot etf flow analysis",       0.20, 1,    10),
        ("linkedin", "btc spot etf flow analysis",       0.45,  8,   50),
        ("reddit",   "btc spot etf flow analysis",       0.62, 20,  180),
        ("substack", "btc spot etf flow analysis",       0.74,  9,   55),

        # ARBITRAGE: high on substack, low on tiktok & linkedin
        ("substack", "perp basis decay 101",             0.81,  4,   22),
        ("youtube",  "perp basis decay 101",             0.55,  6,   80),
        ("twitter",  "perp basis decay 101",             0.60, 11,  220),
        ("tiktok",   "perp basis decay 101",             0.10, 0,     0),
        ("linkedin", "perp basis decay 101",             0.08, 0,     0),
        ("reddit",   "perp basis decay 101",             0.42,  3,   18),

        ("reddit",   "exchange counterparty risk",       0.72, 14,  240),
        ("twitter",  "exchange counterparty risk",       0.68, 19,  410),
        ("youtube",  "exchange counterparty risk",       0.40,  5,   30),
        ("tiktok",   "exchange counterparty risk",       0.05, 0,     0),
        ("linkedin", "exchange counterparty risk",       0.55,  7,   45),
        ("substack", "exchange counterparty risk",       0.58,  4,   20),

        ("tiktok",   "60 sec liquidation cascade",       0.92, 35,  450),
        ("youtube",  "60 sec liquidation cascade",       0.70, 18,  220),
        ("twitter",  "60 sec liquidation cascade",       0.62, 20,  340),
        ("reddit",   "60 sec liquidation cascade",       0.35,  4,   25),
        ("linkedin", "60 sec liquidation cascade",       0.08, 0,     0),
        ("substack", "60 sec liquidation cascade",       0.15, 1,     5),
    ],

    "home_automation": [
        ("youtube",  "home assistant zigbee setup",      0.80, 28,  500),
        ("reddit",   "home assistant zigbee setup",      0.75, 32,  410),
        ("twitter",  "home assistant zigbee setup",      0.25,  6,   30),
        ("tiktok",   "home assistant zigbee setup",      0.55,  9,   60),
        ("linkedin", "home assistant zigbee setup",      0.05, 0,     0),
        ("substack", "home assistant zigbee setup",      0.18,  2,    8),

        ("youtube",  "matter protocol vs zigbee",        0.72, 18,  300),
        ("reddit",   "matter protocol vs zigbee",        0.78, 22,  290),
        ("substack", "matter protocol vs zigbee",        0.65,  3,   18),
        ("twitter",  "matter protocol vs zigbee",        0.40,  9,   55),
        ("tiktok",   "matter protocol vs zigbee",        0.10, 0,     0),
        ("linkedin", "matter protocol vs zigbee",        0.30,  4,   20),

        ("reddit",   "frigate nvr ai cameras",           0.81, 16,  220),
        ("youtube",  "frigate nvr ai cameras",           0.85, 20,  380),
        ("substack", "frigate nvr ai cameras",           0.40,  2,    8),
        ("twitter",  "frigate nvr ai cameras",           0.35,  5,   28),
        ("tiktok",   "frigate nvr ai cameras",           0.62,  4,   32),
        ("linkedin", "frigate nvr ai cameras",           0.08, 0,     0),

        ("youtube",  "esphome thermostat diy",           0.74,  8,  140),
        ("reddit",   "esphome thermostat diy",           0.70, 11,  180),
        ("substack", "esphome thermostat diy",           0.30,  1,    4),
        ("tiktok",   "esphome thermostat diy",           0.10, 0,     0),
    ],

    "indie_saas": [
        ("twitter",  "pricing page conversion",          0.86, 28,  720),
        ("linkedin", "pricing page conversion",          0.78, 22,  380),
        ("youtube",  "pricing page conversion",          0.55,  6,   55),
        ("substack", "pricing page conversion",          0.72, 11,   90),
        ("reddit",   "pricing page conversion",          0.50,  8,   40),
        ("tiktok",   "pricing page conversion",          0.05, 0,     0),

        ("twitter",  "cold outbound to enterprise",      0.81, 24,  610),
        ("linkedin", "cold outbound to enterprise",      0.85, 30,  790),
        ("youtube",  "cold outbound to enterprise",      0.30,  4,   20),
        ("substack", "cold outbound to enterprise",      0.62,  7,   45),
        ("reddit",   "cold outbound to enterprise",      0.18,  2,    8),
        ("tiktok",   "cold outbound to enterprise",      0.02, 0,     0),

        ("linkedin", "free trial vs freemium",           0.74, 14,  220),
        ("twitter",  "free trial vs freemium",           0.78, 19,  340),
        ("youtube",  "free trial vs freemium",           0.40,  3,   20),
        ("substack", "free trial vs freemium",           0.68,  5,   30),
        ("reddit",   "free trial vs freemium",           0.55,  6,   25),
        ("tiktok",   "free trial vs freemium",           0.05, 0,     0),

        ("twitter",  "shipping in public weekly",        0.72, 30,  600),
        ("linkedin", "shipping in public weekly",        0.58, 14,  150),
        ("youtube",  "shipping in public weekly",        0.45,  7,   40),
        ("substack", "shipping in public weekly",        0.60,  9,   50),
    ],

    "longevity": [
        ("youtube",  "zone 2 cardio protocol",           0.84, 22,  410),
        ("twitter",  "zone 2 cardio protocol",           0.70, 18,  280),
        ("substack", "zone 2 cardio protocol",           0.65,  8,   45),
        ("tiktok",   "zone 2 cardio protocol",           0.62, 11,  140),
        ("linkedin", "zone 2 cardio protocol",           0.18,  2,    8),
        ("reddit",   "zone 2 cardio protocol",           0.55, 14,  120),

        ("youtube",  "rapamycin off-label dosing",       0.79, 12,  250),
        ("substack", "rapamycin off-label dosing",       0.82,  9,   80),
        ("twitter",  "rapamycin off-label dosing",       0.66, 14,  180),
        ("tiktok",   "rapamycin off-label dosing",       0.10, 1,    5),
        ("linkedin", "rapamycin off-label dosing",       0.05, 0,    0),
        ("reddit",   "rapamycin off-label dosing",       0.60,  8,   45),

        ("youtube",  "cgm without diabetes",             0.76, 16,  300),
        ("tiktok",   "cgm without diabetes",             0.80, 19,  340),
        ("substack", "cgm without diabetes",             0.55,  4,   18),
        ("twitter",  "cgm without diabetes",             0.50, 11,   90),
        ("linkedin", "cgm without diabetes",             0.20,  3,   12),
        ("reddit",   "cgm without diabetes",             0.48,  9,   55),
    ],

    "ai_engineering": [
        ("twitter",  "prompt cache cost optimization",   0.83, 26,  540),
        ("youtube",  "prompt cache cost optimization",   0.60,  8,   80),
        ("substack", "prompt cache cost optimization",   0.78, 11,   80),
        ("linkedin", "prompt cache cost optimization",   0.45,  9,   55),
        ("reddit",   "prompt cache cost optimization",   0.62, 12,   95),
        ("tiktok",   "prompt cache cost optimization",   0.05, 0,    0),

        ("twitter",  "eval-driven agent dev",            0.79, 21,  410),
        ("substack", "eval-driven agent dev",            0.82,  9,   65),
        ("youtube",  "eval-driven agent dev",            0.55,  6,   45),
        ("linkedin", "eval-driven agent dev",            0.40,  7,   30),
        ("reddit",   "eval-driven agent dev",            0.58, 10,   70),

        ("youtube",  "rag vs long context tradeoffs",    0.74, 14,  200),
        ("twitter",  "rag vs long context tradeoffs",    0.80, 19,  340),
        ("substack", "rag vs long context tradeoffs",    0.71,  8,   55),
        ("reddit",   "rag vs long context tradeoffs",    0.62, 11,   80),
        ("linkedin", "rag vs long context tradeoffs",    0.38,  6,   25),
        ("tiktok",   "rag vs long context tradeoffs",    0.04, 0,    0),
    ],

    "personal_finance": [
        ("tiktok",   "tax loss harvesting basics",       0.75, 22,  410),
        ("youtube",  "tax loss harvesting basics",       0.78, 18,  340),
        ("twitter",  "tax loss harvesting basics",       0.55, 11,   80),
        ("substack", "tax loss harvesting basics",       0.70,  9,   55),
        ("linkedin", "tax loss harvesting basics",       0.40,  6,   25),
        ("reddit",   "tax loss harvesting basics",       0.65, 14,  120),

        ("youtube",  "i-bonds vs tips deep dive",        0.72, 11,  180),
        ("substack", "i-bonds vs tips deep dive",        0.81,  6,   40),
        ("twitter",  "i-bonds vs tips deep dive",        0.50,  8,   50),
        ("reddit",   "i-bonds vs tips deep dive",        0.60, 12,   85),
        ("linkedin", "i-bonds vs tips deep dive",        0.30,  4,   15),
        ("tiktok",   "i-bonds vs tips deep dive",        0.20,  2,   10),

        ("tiktok",   "high yield savings shifts",        0.82, 28,  500),
        ("youtube",  "high yield savings shifts",        0.65, 12,   90),
        ("twitter",  "high yield savings shifts",        0.45,  9,   45),
        ("substack", "high yield savings shifts",        0.55,  5,   25),
        ("linkedin", "high yield savings shifts",        0.30,  3,   12),
        ("reddit",   "high yield savings shifts",        0.50,  8,   40),
    ],
}


def get_signals(niche: str | None = None) -> list[PlatformSignal]:
    """Return all signals, or only for a specific niche."""
    out: list[PlatformSignal] = []
    items = _SEEDS.items() if niche is None else [(niche, _SEEDS.get(niche, []))]
    for n, rows in items:
        for plat, topic, eng, supply, sample in rows:
            out.append(PlatformSignal(
                platform=plat,  # type: ignore[arg-type]
                niche=n,
                topic=topic,
                engagement_score=eng,
                supply_count=supply,
                sample_size=sample,
            ))
    return out


def list_niches() -> list[str]:
    return list(NICHES)
