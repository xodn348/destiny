<p align="center">
  <img src="assets/hero.png" alt="destiny — a real fortune skill for Claude Code" width="700">
</p>

<h1 align="center">destiny</h1>

<p align="center">
  A real fortune-telling skill for <a href="https://claude.com/claude-code">Claude Code</a>.<br>
  Not a horoscope generator. The numbers are computed; only the interpretation is generative.
</p>

---

## Quick start

```
/plugin marketplace add xodn348/destiny
/plugin install destiny@destiny-marketplace
/destiny
```

That's it. The first call asks for your birth date, time, city, and gender — once. Every call after is one word: `/destiny`.

## How it flows

```
Claude Code
   │
   ▼
destiny plugin            ← installed once via /plugin install
   │
   ▼
/destiny skill            ← invoked any time
   │
   ▼
your birth info           ← asked once, saved to ~/.destiny/profile.json
   │
   ▼
destiny of the day        ← personalized reading: today's fortune + life reading
```

## What you get

Each `/destiny` produces a two-section reading:

**🔮 Today's Fortune** — a short prose reading of today against your chart, with five-category stars (overall, love, money, career, health), a hexagram drawn for this moment, and lucky number / color / direction.

**🌌 Life Reading** — your character, the broad arc of your life, and where you are in the current 10-year period. Plain language, no untranslated jargon.

## What's actually computed (vs. invented)

| Layer | Source |
|---|---|
| 사주 8 characters from your birth | `lunar-python` (real 만세력, equivalent to KASI national calendar) |
| True solar time correction | longitude offset from KST (1° = 4 min) |
| Korean DST handling (1987–88) | auto |
| Today's day pillar (일진) | `lunar-python` |
| Five Elements + Ten Gods (십신) | classical 60-cycle lookup tables |
| Branch interactions (합·충·형) | classical lookup tables |
| I-Ching hexagram for the moment | 매화역수 시점법 (plum-blossom time divination) |
| Hexagram corpus | King Wen ordering, Legge (1899) public-domain translation |
| Lucky number / color / direction | derived from your day master + hexagram |
| **Star ratings + character + life arc + advice** | **Claude, applying classical 명리 knowledge to the data above** |

Same person + same day = identical script output, every time. Only the prose phrasing changes.

No external APIs, no scraped sites. Everything runs locally.

## Variants

- `/destiny` — full reading (auto-loaded profile)
- `/destiny today` — only today's fortune
- `/destiny life` — only life reading
- `/destiny reset` — delete saved profile and start over
- `/destiny in english|korean|japanese|chinese|spanish` — switch language
- `/destiny born YYYY-MM-DD HH:MM <city> <m|f>` — one-off without saving
- `/destiny quick` — generic daily, no personal data

## Why this exists

Most fortune apps either (a) use real 만세력 calculation but hide proprietary interpretation rules behind a paywall, or (b) generate everything with an LLM and call it astrology. This skill keeps the deterministic part deterministic (you can verify your 사주 against any Korean 만세력 site) and lets Claude do what it's actually good at — applying classical 명리 reading conventions to that fixed data.

Default output is English with all 한자 / 명리 terms unpacked into plain language. A foreigner with zero exposure to 사주 should follow it. Korean output keeps the terse traditional terms.

## Stack

- Python 3.10+
- [`lunar-python`](https://github.com/6tail/lunar-python) (MIT) — pure-Python lunar calendar engine
- I-Ching: King Wen ordering + Legge (1899) public-domain judgments
- Claude Code plugin format

## License

MIT
