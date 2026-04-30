# destiny

A real fortune-telling skill for [Claude Code](https://claude.com/claude-code). Type `/destiny` and you get today's fortune instantly — no questions asked, no LLM hallucination. The numbers are computed; only the interpretation is generative.

```
🔮 Today's Fortune — 2026-04-30 (Thursday)

The day's energy is Wood (甲戌). A pushing-outward kind of day —
ideas want to leave the desk and meet someone.

⭐ Overall ★★★★☆
The path is open. Don't overthink the next small step.

💕 Love ★★★☆☆
A short message lands more than a long one today.

💰 Money ★★★★☆
A small gain through someone close — accept it gracefully.

💼 Career & Studies ★★★★★
The thing you've been stuck on starts to move. Around 3 PM, watch.

🌿 Health ★★★☆☆
Eyes and shoulders carry today's weight. Step away from the screen.

☯ Hexagram for this moment
19. Approach (지택림 · 臨)
☷ Earth over ☱ Lake, moving line 4
"The great approaches; in eighth month, decline."

A door opens. Walk through it now — the favorable window is real
but won't last forever.

---
🍀 Lucky number: 46
🎨 Lucky color: Forest green
🧭 Lucky direction: East
✨ Words for today: "Move while the door is open."
```

## Install

This repo is both a Claude Code **plugin** and a single-plugin **marketplace**:

```
/plugin marketplace add xodn348/destiny
/plugin install destiny@destiny-marketplace
```

Or locally:

```
/plugin marketplace add ~/code/destiny
```

The skill auto-installs `lunar-python` on first run.

## Usage

```
/destiny
```

That's it. You get today's fortune.

Optional — if you want a **personal birth-chart reading** (Four Pillars / BaZi):

```
/destiny born 1992-08-15 14:30 Seoul male
```

Other variants:
- `/destiny iching` — just the hexagram + lucky items
- `/destiny in korean` (or japanese / chinese / spanish) — switch language

## What's actually computed

A Python script computes the deterministic parts. Claude only writes the prose.

| What | How |
|---|---|
| Today's date / day pillar | [`lunar-python`](https://github.com/6tail/lunar-python) — real 만세력 |
| One I-Ching hexagram for now | 매화역수 시점법 (plum-blossom time divination) from lunar 연/월/일/시 |
| Lucky number | Hexagram number × matter-of-time sum, mod 100 |
| Lucky color & direction | Day pillar's element (Wood/Fire/Earth/Metal/Water) |
| Hexagram corpus | King Wen ordering, Legge (1899) judgments — public domain |

Personal mode adds the Four Pillars chart with all classical corrections:

| Correction | Applied |
|---|---|
| Solar→lunar conversion | ✅ |
| 24 solar terms for month pillar | ✅ |
| True solar time by birthplace longitude | ✅ (1° = 4 min) |
| Korean DST 1987-05-10 ~ 1988-10-09 | ✅ auto |
| 야자시(default) vs 조자시 | ✅ selectable |
| Ten Gods (십신) relationships | ✅ |
| 10-year luck cycles (대운) | ✅ |

No external API calls. Everything runs locally.

## Stack

- Python 3.10+
- [`lunar-python`](https://github.com/6tail/lunar-python) (MIT) — pure-Python lunar calendar engine
- I-Ching data: King Wen ordering + Legge (1899) public-domain judgments

## License

MIT
