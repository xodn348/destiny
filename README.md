# destiny

A daily fortune-telling skill for [Claude Code](https://claude.com/claude-code).

Invoke `/destiny` and get a structured daily fortune across five categories — Overall, Love, Money, Career & Studies, Health — plus a lucky number, color, and direction.

```
🔮 Today's Fortune — 2026-04-30 (Thursday)

⭐ Overall ★★★★☆
The morning may feel a little stuck, but things start flowing after lunch.

💕 Love ★★★☆☆
Don't read too much into a small remark from someone close to you.

💰 Money ★★★★☆
An unexpected refund or small bonus may land today.

💼 Career & Studies ★★★★★
Around 3 PM, the problem you've been stuck on starts to unravel.

🌿 Health ★★★☆☆
Shoulders and neck stiffen easily today — stretch, even briefly.

---
🍀 Lucky number: 27
🎨 Lucky color: Deep teal
🧭 Lucky direction: Southeast
✨ Words for today: "Slow down when you're rushed"
```

The skill defaults to Korean output (오늘의 운세 format) and switches to English on request.

## Install

This repo is both a Claude Code **plugin** and a single-plugin **marketplace**. Add it as a marketplace, then install the plugin:

```
/plugin marketplace add xodn348/destiny
/plugin install destiny@destiny-marketplace
```

Or, after cloning locally:

```
/plugin marketplace add ~/code/destiny
```

## Usage

```
/destiny
```

Variants:
- `/destiny love only` — focus on a single category
- `/destiny tiger born 1992` — incorporate zodiac / birth year
- `/destiny in english` — English output (default is Korean)

## How it works

When invoked, the skill anchors the reading to today's real date (via `date`), then produces a balanced fortune — never all 5-stars, never doom-saying, no disclaimers. Same date + same user stays consistent within a session; different dates produce clearly different readings.

## License

MIT
