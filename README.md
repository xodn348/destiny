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

### Prerequisites

- [Claude Code](https://claude.com/claude-code) **v2.0 or newer**
  - Check with `claude --version`
  - Update with `npm i -g @anthropic-ai/claude-code`
- The `/plugin` command must be available. On modern Claude Code it's on by default. If `/plugin` isn't recognized inside Claude Code, run `/config` and enable Plugins, then restart Claude Code.

### Install (inside Claude Code)

```
/plugin marketplace add xodn348/destiny
/plugin install destiny@destiny-marketplace
/destiny
```

### Install from terminal (fallback if `/plugin` isn't available)

```bash
claude plugin marketplace add xodn348/destiny
claude plugin install destiny@destiny-marketplace
```

Then launch Claude Code and run `/destiny`.

### Verify

```bash
claude plugin list   # should show: destiny@destiny-marketplace
```

That's it. The first `/destiny` call asks for your birth date, time, city, and gender — once. Every call after is just `/destiny`.

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
your birth date           ← asked once, saved to ~/.destiny/profile.json
   │
   ▼
destiny of the day        ← personalized: today's fortune + life reading
```

## What you get

Each `/destiny` produces a two-section reading:

**🔮 Today's Fortune** — a short prose reading of today against your birth chart, with five-category stars (overall, love, money, career, health), a hexagram drawn for this moment, and a lucky number / color / direction.

**🌌 Life Reading** — your character, the broad arc of your life, and where you are in your current 10-year period. Plain language, no untranslated jargon.

## Example output

<p align="center">
  <img src="assets/example.png" alt="Sample /destiny reading" width="700">
</p>

<p align="center"><sub>Real run from a sample profile (1992-07-31, Suwon). Same person + same day always produces identical script output; only the prose phrasing changes between calls.</sub></p>

## How it works (the principles in 60 seconds)

This skill uses three pieces of classical East Asian metaphysics, each computed deterministically from your birth date and time:

- **Four Pillars (the eight-character birth chart)** — Your year, month, day, and hour of birth each map to a pair of Chinese characters (one "Heavenly Stem" + one "Earthly Branch") drawn from a 60-cycle calendar that has run continuously for over two millennia. The eight characters together describe your "elemental fingerprint": which of the five elements (Wood / Fire / Earth / Metal / Water) dominate, which are missing, and how they relate. The character of your day-of-birth is your "core self".

- **Perpetual lunar calendar** — The engine that converts solar dates to the eight characters. It handles solar terms (the 24 climate divisions of the year), lunar/solar conversion, true-solar-time correction by birthplace longitude, and Korean Daylight Saving for births in 1987–88. Equivalent to the calendar published by Korea's national astronomical observatory.

- **The I-Ching (Book of Changes)** — A 3,000-year-old divination system of 64 hexagrams. We draw one hexagram for the present moment using *plum-blossom time divination* — an algorithm by the Song-dynasty scholar Shao Yong that derives the hexagram from the current lunar date and hour. Hexagram texts are from James Legge's 1899 public-domain translation.

The skill computes today's "day pillar" the same way and analyzes its relationship with your birth chart — five-element generation/control cycles, branch harmonies and clashes — to produce the reading.

## What's actually computed (vs. interpreted by Claude)

| Layer | Source |
|---|---|
| Your eight-character birth chart | [`lunar-python`](https://github.com/6tail/lunar-python) — pure-Python perpetual calendar |
| True solar time correction | longitude offset from local standard time meridian (1° = 4 min) |
| Korean DST handling (1987–88) | automatic |
| Today's day pillar | `lunar-python` |
| Five Elements + Ten Gods relationships | classical 60-cycle lookup tables |
| Branch harmonies, clashes, punishments | classical lookup tables |
| I-Ching hexagram for this moment | plum-blossom time divination |
| Hexagram corpus | King Wen ordering, Legge (1899) public-domain translation |
| Lucky number / color / direction | derived from your day-of-birth's element + the hexagram |
| **Star ratings, character sketch, life arc, today's advice** | **Claude, applying classical reading conventions to the data above** |

Same person + same day always produces identical script output. Only the prose phrasing changes between calls.

No external APIs. No scraped sites. Everything runs locally.

## Variants

- `/destiny` — full reading (auto-loads saved profile)
- `/destiny today` — only today's fortune
- `/destiny life` — only life reading
- `/destiny reset` — delete saved profile and start over
- `/destiny in english|korean|japanese|chinese|spanish` — switch language
- `/destiny born YYYY-MM-DD HH:MM <city> <m|f>` — one-off without saving
- `/destiny quick` — generic daily, no personal data
- `/destiny compat <partner birth> <city> <m|f>` — couple compatibility (궁합) reading using two charts
- `/destiny hook on` / `/destiny hook off` — auto-run `/destiny` on every Claude Code session start (opt-in)

## Auto-run on session start (optional)

If you want `/destiny` to fire every time you launch Claude Code — like a morning paper — run `/destiny hook on` once. To turn it off, `/destiny hook off`. Both commands edit `~/.claude/settings.json` safely (your other hooks are preserved, and a backup is saved to `~/.claude/settings.json.destiny-backup` before the first install).

If you'd rather wire it manually, add this to `~/.claude/settings.json`:

```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "*",
        "hooks": [{"type": "command", "command": "claude --print '/destiny'"}]
      }
    ]
  }
}
```

## About

A Claude Code plugin for daily fortune readings. Your birth chart and today's day pillar are computed locally by a Python perpetual lunar calendar (`lunar-python`) — the same math used by traditional almanacs. Claude only translates those fixed numbers into prose, using documented classical reading conventions.

Not scientifically validated; not advice. For fun. See **Safety & disclaimer** below. Default English; Korean / Japanese / Chinese / Spanish on request.

## Stack

- Python 3.10+
- [`lunar-python`](https://github.com/6tail/lunar-python) (MIT) — pure-Python perpetual lunar calendar
- I-Ching: King Wen ordering + Legge (1899) public-domain judgments
- Claude Code plugin format

## Safety & disclaimer

**For entertainment only. No scientific basis. Not advice.**

`destiny` is a personal entertainment project rooted in classical East Asian metaphysics (Four Pillars / I-Ching). The chart calculations are deterministic and the prose is written by Claude on top of that fixed data — but the **underlying system has no scientifically established predictive validity**, and the readings are not predictions of anything real.

**This is not professional advice of any kind.** Specifically, nothing produced by this tool is or should be treated as: medical, psychological, psychiatric, financial, investment, legal, employment, relationship, or any other professional advice. Do not make life decisions based on a reading. Do not use it as a substitute for consulting a qualified professional or for talking to a real human in your life when something matters.

**Mental-health crisis.** If you are in crisis or having thoughts of self-harm, please contact a qualified professional immediately. International directory of crisis lines: <https://findahelpline.com>.

**Intended audience.** This tool is intended for adults who understand it is a recreational reading.

**No warranty, no liability.** This software is provided "AS IS", without warranty of any kind, express or implied — see the LICENSE file for the full text. The author and contributors **disclaim all liability** for any direct, indirect, incidental, consequential, or other damages or harm — financial, emotional, relational, professional, or otherwise — arising out of or in connection with the use, reliance on, or inability to use this software or any reading it produces. By using this tool you agree that you do so **at your own risk and on your own discretion**.

**Local laws.** Fortune-telling and divination are regulated in some jurisdictions. You are responsible for ensuring your use of this tool complies with the laws applicable to you.

## License

MIT
