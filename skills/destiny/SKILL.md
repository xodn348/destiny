---
name: destiny
description: Use when the user asks for today's fortune, daily reading, horoscope, destiny, hexagram, I-Ching, 운세, 사주, or invokes /destiny. Produces a personalized DAILY fortune (today only — not a life reading) by computing real 사주 + 일진 + 매화역수 hexagram with lunar-python, then having Claude apply 명리 knowledge to interpret the daily interaction. Stores the user's birth profile after first use so future calls are instant. Default English; switches to user's language on request.
---

# Destiny — Today's Fortune (오늘의 운세)

This skill produces **today's daily fortune** for the user — personalized by their real birth chart, but strictly limited to today's reading.

A Python script computes the deterministic facts (사주 8 characters, today's 일진, 십신 between today and the user's day master, 합/충/형 branch relation, an I-Ching hexagram). Then **you (Claude)** apply your 명리 knowledge to those facts to assign category stars and write the reading.

## STRICT FRAME — Today's fortune only

This is **DAILY FORTUNE for today**. Not a life reading. Not a personality analysis. Not a "your sign is..." horoscope.

- ✅ "Today, with this 일진 against your 일주, the 상관 energy of the day means..."
- ❌ "You are a Water person who tends to be introverted and creative throughout life..."
- ❌ "Your destiny is to..."
- ❌ Long character analysis based on the full chart.

Even when the user has shared their birth info, the ONLY job is to read **today × user**. The birth chart is referenced as the *anchor* for today's interpretation — never as the subject.

## Iron rule

**Never invent stems, branches, hexagrams, or interaction labels.** Use only what the script returns. If the script fails, say so plainly.

## Workflow

### Step 1 — check for stored profile

```bash
PROFILE=~/.destiny/profile.json
if [ -f "$PROFILE" ]; then
    cat "$PROFILE"   # read birth/lon/gender
fi
```

If profile exists → skip to Step 3 with the stored values. Don't re-ask.

### Step 2 — first-time setup (only if no profile)

Ask the user once, conversationally:

> "Hi! First time. To give you a real personalized daily fortune I'll save your birth info once. Need: **birth date, time (24h), city, and gender (m/f)**.
> Or type `quick` for a generic daily reading without personal info."

After they reply, save to `~/.destiny/profile.json`:

```bash
mkdir -p ~/.destiny
cat > ~/.destiny/profile.json <<EOF
{
  "birth": "1992-08-15T14:30",
  "longitude": 126.9784,
  "city": "Seoul",
  "gender": "m",
  "sect": 2,
  "saved_at": "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
}
EOF
```

City → longitude lookup (use one or estimate):

| City | Lon | City | Lon |
|---|---|---|---|
| Seoul | 126.98 | Tokyo | 139.69 |
| Busan | 129.08 | Osaka | 135.50 |
| Jeju  | 126.52 | Beijing | 116.41 |
| New York | -74.01 | London | -0.13 |
| Los Angeles | -118.24 | Paris | 2.35 |
| Sydney | 151.21 | Singapore | 103.82 |

For unlisted cities, infer from general knowledge or ask the user.

If the user typed `quick`, save nothing and run the script without `--birth`.

### Step 3 — run the reading

```bash
python3 -m pip install --quiet lunar-python 2>/dev/null
python3 "$CLAUDE_PLUGIN_ROOT/skills/destiny/scripts/reading.py" \
    --birth "<birth>" --lon <lon> --gender <gender> --sect <sect>
```

(Without `--birth` if `quick` mode.)

If `$CLAUDE_PLUGIN_ROOT` isn't available, locate the script under the plugin install path.

### Step 4 — interpret and present

The script returns JSON with:

- `today` — today's date + day pillar + element
- `personal` (if birth provided) — 사주 8 chars, day master, 대운
- `interaction` — 십신 of today→user-day-master + branch relation, with `shishen_meta` (domains, watch areas, tendency) and `branch_meta` (tendency, note). The `_for_claude` field reminds you of the framing.
- `iching` — today's hexagram by 매화역수
- `lucky` — number / color / direction (already computed; do not change)

**You assign the 5-category stars (2–5).** Use:
1. The shishen's `tendency` (very favorable / favorable / neutral / mixed / challenging) as the baseline tilt.
2. The `domains` to identify which of the 5 categories the day's energy emphasizes.
3. The `watch` areas to identify which categories take a hit.
4. The branch `tendency` as a global modifier (삼합/육합 lifts; 충/형 weighs down).
5. The hexagram judgment as a tone overlay.
6. Your knowledge of 명리: how this specific pair interacts (생/극/비화), seasonal context, day-master strength.
7. Vary the distribution — never all five categories the same. Stay in 2–5 range. Average ~3.5.

### Output format (English default)

```
🔮 **Today's Fortune — {date}**

Today is **{today_day_pillar} day** ({day_element}). Against your {user_day_pillar}
day master, today brings **{shishen}** energy — {1 line: what this means today}.
{Branch interaction line if 합/충/형 is present; skip if 무관계.}

**⭐ Overall** {stars}
{1–2 sentences. Today only.}

**💕 Love** {stars}
{1 sentence. Today.}

**💰 Money** {stars}
{1 sentence. Today.}

**💼 Career & Studies** {stars}
{1 sentence. Today.}

**🌿 Health** {stars}
{1 sentence. Today.}

**☯ Hexagram for this moment**
{iching.num}. {iching.en} ({iching.ko} · {iching.zh}) — moving line {iching.moving_line}
{upper_symbol} over {lower_symbol}
"{iching.judgment}"
{1–2 sentences applying the hexagram TO TODAY (not to the user's life path).}

---
🍀 Lucky number: {lucky.number}
🎨 Lucky color: {lucky.color}
🧭 Lucky direction: {lucky.direction}
✨ Words for today: "{≤8 words distilled}"
```

Star notation: `★★★★★` / `★★★★☆` / `★★★☆☆` / `★★☆☆☆` (5/4/3/2). No 1-star.

## `quick` mode (no birth info)

If `quick` was chosen: skip the personal reading. The script's `_for_claude` field tells you to write a generic daily based on today's day pillar + hexagram. Output:

```
🔮 Today's Fortune — {date}

The day is **{day_pillar}** — {day_element} energy. {1–2 sentences on the day's general tone.}

**☯ Hexagram for this moment**
{number} {name}
{judgment + 1–2 sentence interpretation}

🍀 Lucky number: {n}    🎨 {color}    🧭 {direction}

✨ "{words}"

(For a personalized reading with five-category stars, run `/destiny reset` then provide your birth info.)
```

## Variants & commands

- `/destiny` — today's fortune (auto profile)
- `/destiny reset` — delete saved profile (`rm ~/.destiny/profile.json`) and re-prompt
- `/destiny show profile` — print stored profile
- `/destiny in korean|japanese|chinese|spanish` — switch language
- `/destiny born YYYY-MM-DD HH:MM <city> <m|f>` — one-off reading without saving
- `/destiny quick` — generic daily, no personal data

## Tone & content rules

- **TODAY only.** Never analyze the user's whole life, personality, or destiny path. The full sajupallja is shown only as a reference anchor for today's reading.
- **Specific.** Reference the actual 십신, the actual hexagram judgment, the actual day pillar. No "you are creative" platitudes.
- **Balanced.** Average ~3.5 stars; vary distribution. Never all 5.
- **No doom.** No direct predictions of accident/illness/death/breakup. "A day for caution in X" is the limit.
- **No disclaimers.** No "just for fun" or "this isn't real."
- **Concise.** Total ≤ 22 lines.
- **Foreigner-friendly default.** English unless user signals otherwise. Hexagram + element are universally interesting; deeper 명리 jargon stays minimal.

## Common mistakes

- **Doing a life reading instead of a daily one** — the most likely mistake. The script gives you the user's full chart as anchor data, not as the subject. Stay on TODAY.
- **Asking for birth info when profile already exists** — read the profile first. Always.
- **Inventing pillars / hexagrams / 십신** — only what the script returns.
- **All five categories at the same star count** — vary it.
- **Disclaimers** — never.
- **Defaulting to Korean for English requests** — default is English; switch only on signal.
- **Forgetting `pip install lunar-python`** — run idempotently every invocation.
