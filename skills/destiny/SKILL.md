---
name: destiny
description: Use when the user asks for today's fortune, daily reading, horoscope, destiny, hexagram, I-Ching, 운세, 사주, or invokes /destiny. By default produces today's fortune instantly (no birth info needed) — backed by a real lunar calendar engine and an I-Ching hexagram drawn for the current moment. If the user provides a birth date+time, also produces a personalized chart reading. Default language English; switches to user's language on request.
---

# Destiny — daily fortune, real lunar engine

This skill produces a **real fortune reading**, not a free-form LLM guess. A Python script computes:

- **Today's day pillar** (Heavenly Stem + Earthly Branch) from the lunar calendar
- **One I-Ching hexagram** for this moment via 매화역수 시점법 (plum-blossom time divination)
- **Lucky number/color/direction** derived from the day pillar's element

If the user supplies a birth date+time, the script also produces a real **personal birth chart** (Four Pillars / BaZi) with proper true-solar-time correction, DST handling, and Ten Gods analysis.

You then interpret the structured numbers into a warm, specific reading.

## Iron rule

**Never invent stems, branches, or hexagrams.** Use only what the script returns. If the script fails, say so plainly — do not fabricate.

## Default behavior — `/destiny` with no arguments

**Do not ask for birth info.** Just run the daily reading immediately.

### 1. Run the script

```bash
python3 -m pip install --quiet lunar-python 2>/dev/null
python3 "$CLAUDE_PLUGIN_ROOT/skills/destiny/scripts/reading.py"
```

If `$CLAUDE_PLUGIN_ROOT` isn't set, locate the script under the plugin install path (typically `~/.claude/plugins/cache/.../destiny/skills/destiny/scripts/reading.py`).

The script returns JSON with: `today`, `iching`, `lucky`.

### 2. Output format (English default)

```
🔮 **Today's Fortune — {date}**

The day's energy is **{day_element}** ({day_pillar}).
{1–2 sentences: tone of the day given the element + day pillar.}

**⭐ Overall** {stars}
{1–2 sentences. Ground in the hexagram judgment + today's element.}

**💕 Love** {stars}
{1 sentence}

**💰 Money** {stars}
{1 sentence}

**💼 Career & Studies** {stars}
{1 sentence}

**🌿 Health** {stars}
{1 sentence}

**☯ Hexagram for this moment**
{iching.num}. {iching.en} ({iching.ko} · {iching.zh})
{upper_symbol} over {lower_symbol}, moving line {moving_line}
"{iching.judgment}"
{1–2 sentences applying the hexagram to today.}

---
🍀 Lucky number: {lucky.number}
🎨 Lucky color: {lucky.color}
🧭 Lucky direction: {lucky.direction}
✨ Words for today: "{≤8 words distilled from above}"
```

Star notation: `★★★★★` / `★★★★☆` / `★★★☆☆` / `★★☆☆☆` (5/4/3/2). Never 1 star. Vary across the five categories — never all the same number.

## Personal mode — when the user gives birth info

If the user invokes with birth info — `/destiny born 1992-08-15 14:30 Seoul male` — or asks for a personal/birth-chart reading, run with `--birth`:

```bash
python3 reading.py --birth 1992-08-15T14:30 --lon 126.9784 --sect 2 --gender m
```

Longitude lookup table (use one or estimate from city):

| City | Lon | City | Lon |
|---|---|---|---|
| Seoul | 126.98 | Tokyo | 139.69 |
| Busan | 129.08 | Osaka | 135.50 |
| Jeju | 126.52 | Beijing | 116.41 |
| New York | -74.01 | London | -0.13 |
| Los Angeles | -118.24 | Paris | 2.35 |

Default to Seoul (126.98) if the user only says "Korea" or doesn't specify. Ask for the city only if the user explicitly wants accuracy and didn't mention one.

The script then also returns a `personal` block with `pillars`, `day_master`, `shishen`, `da_yun`. Append a section to the daily output:

```
**🪪 Your birth chart**
- Year   {pillars.year.gz} ({ko}, {nayin})
- Month  {pillars.month.gz} ({ko}, {nayin})
- Day    {pillars.day.gz} ({ko}, {nayin}) ← Day master: {day_master} ({day_master_element})
- Hour   {pillars.hour.gz} ({ko}, {nayin})

Lunar birth: {lunar_birth}
Adjustments: true-solar {offset_min}min, DST={true|false}, hour-rule={야자시|조자시}

{2–3 sentences: dominant element, key Ten God, character tone.}

**Today × your chart**
{Look at interaction_with_user — if today's day pillar 합/충/형/파/해 with user's day pillar, mention it. Otherwise describe how today's element relates to user's day master (생/극/비화).}

**Current 10-year cycle**
You're in {da_yun cycle whose start_year ≤ today's year < next start_year}: {ganzhi} ({ko}).
{1 sentence on the cycle's tone.}
```

## Variants

- `/destiny iching` — show only the I-Ching block + lucky items
- `/destiny in korean` / `/destiny in japanese` / etc. — switch output language; keep stems/hexagram characters intact
- `/destiny born YYYY-MM-DD HH:MM <city> <m|f>` — personal mode inline

## Tone & content rules

- **Specific over generic.** Reference the actual hexagram judgment line and today's element — not "you are creative".
- **Balanced.** Average ~3.5–4 stars; never all 5.
- **No doom.** No direct predictions of accident/illness/death/breakup. "A day for caution in X" is the limit.
- **No disclaimers.** Don't write "just for fun" or "this isn't real" — kills the mood.
- **Concise.** Daily reading ≤ 20 lines. With personal block ≤ 35 lines.
- **Foreigner-friendly.** Default English. Hexagram name + element are fine to surface (universally interesting). Hide deep BaZi jargon in personal mode unless the user is clearly Korean or asks for it.

## Language switching

Default: **English**. Switch when:
- User wrote their request in another language → match that language
- User explicitly asks ("in korean", "한국어로", "en español")

For non-English: translate the labels (Today's Fortune, Overall, Love, etc.) but keep the hexagram name characters and stem/branch characters intact — those are data, not text.

## Common mistakes

- **Asking for birth info on default `/destiny`** — don't. Default is no-question instant daily.
- **Inventing pillars or hexagrams** — only use script output. If script errors, say so.
- **All five categories with identical stars** — vary the distribution.
- **Adding a disclaimer** — never.
- **Defaulting to Korean** — default is English; switch only on signal.
- **Forgetting to install lunar-python** — run pip install idempotently every time (no-op if installed).
- **Long, generic readings** — stay under the line budget; tie every line back to the hexagram or element.
