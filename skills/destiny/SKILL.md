---
name: destiny
description: Use when the user asks for a fortune reading, daily destiny, life reading, horoscope, hexagram, I-Ching, 운세, 사주, 명리, or invokes /destiny. Produces TWO sections — (1) today's daily fortune, (2) life destiny from the user's 사주 — written in plain language anyone can follow, with no untranslated jargon. Computes real 사주 + 일진 + 매화역수 hexagram via lunar-python; stores birth profile after first use. Default English.
---

# Destiny — Today's Fortune + Life Reading

`/destiny` produces a reading in two sections, in this order:

1. **🔮 Today's Fortune** — daily 5-category stars + hexagram for this moment
2. **🌌 Life Destiny** — character + life arc + current decade, derived from the user's 사주

**The reading must be readable by someone who has never heard of 사주, 명리, or I-Ching.** Plain, warm, specific language. No untranslated jargon. No reasoning footnotes — those clutter the experience.

## Iron rules

- **Never invent stems, branches, hexagrams, or labels.** Use only what the script returns.
- **Two sections only.** Today's Fortune + Life Destiny. No "Reasoning" section, no debug data dumps.
- **Plain language is mandatory.** Every Chinese character, every 명리/주역 term, must be either (a) skipped entirely or (b) replaced with a short, descriptive English/Korean phrase that conveys what it MEANS, not how it's spelled. See readability rules below.
- **Distinguish today vs life clearly** — never blur them. Today section = today only. Life section = lifelong patterns.

## Workflow

### Step 1 — check for stored profile

```bash
PROFILE=~/.destiny/profile.json
[ -f "$PROFILE" ] && cat "$PROFILE"
```

If profile exists → skip to Step 3 with the stored values.

### Step 2 — first-time setup

> "Hi! First time. To give you a real reading I'll save your birth info once.
> Need: **birth date, time (24h), city, gender (m/f)**.
> Or type `quick` for a generic daily-only reading without personal info."

Save:

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

City → longitude:

| City | Lon | City | Lon |
|---|---|---|---|
| Seoul | 126.98 | Tokyo | 139.69 |
| Suwon | 127.03 | Osaka | 135.50 |
| Busan | 129.08 | Beijing | 116.41 |
| Jeju  | 126.52 | Singapore | 103.82 |
| New York | -74.01 | London | -0.13 |
| LA | -118.24 | Paris | 2.35 |
| Sydney | 151.21 | | |

### Step 3 — run script

```bash
python3 -m pip install --quiet lunar-python 2>/dev/null
python3 "$CLAUDE_PLUGIN_ROOT/skills/destiny/scripts/reading.py" \
    --birth "<birth>" --lon <lon> --gender <gender> --sect <sect>
```

### Step 4 — write the two-section reading

Use the script JSON. Do not echo raw fields. Translate everything into plain language.

## Output format

```
🔮 **Today's Fortune — {date in friendly format, e.g. "Thursday, April 30 2026"}**

{1–2 sentences in plain language describing the day's overall mood and what
the day's energy means specifically for THIS user. Do not say "편관" or
"Seven Killings" — say "today brings a kind of pressure energy that pushes
against your steady, grounded nature".}

**⭐ Overall** {stars}        {1 line, today only, plain language}
**💕 Love** {stars}            {1 line}
**💰 Money** {stars}           {1 line}
**💼 Career** {stars}          {1 line}
**🌿 Health** {stars}          {1 line}

**☯ A reading from the I-Ching for this moment**
{Hexagram name in plain English}, with a small change in the {moving_line}rd line.
"{judgment translated into accessible English, not Legge's archaic phrasing}"
{1–2 sentences applying the hexagram's lesson to TODAY only.}

🍀 Lucky number: {n}    🎨 {color, plainly named}    🧭 {direction in everyday words: "facing east" not just "East"}
✨ "{≤8 words takeaway}"

---

🌌 **Your Life Reading**

**Your core nature**
{2–3 sentences describing the user as a person, derived from their day master
+ chart structure. Plain English. NO "Yang Earth balanced 정인격 살인상생". 
INSTEAD: "You're an Earth-type person — steady, deliberate, the kind of
friend people lean on when things get heavy. The way your chart is built,
outside pressure tends to make you stronger rather than break you."}

**How your life moves**
{2–3 sentences walking through the broad rhythms of life. NO "대운 신해운
상관정재". INSTEAD: "Your twenties were about finding your voice and
building a body of work. Right now (mid-30s through early 40s) is when
that quiet building starts paying off visibly. Your forties and fifties
are when wealth crystallizes."}

**Where you are now**
{2 sentences on the current 10-year period. Name the years (e.g. "2025–2035,
ages 34 to 43"). Describe what this period feels like in plain terms.}

**What helps you most**
{1–2 sentences on the user's "favorable element" but described as a kind of
energy or environment, not as 용신/오행 jargon. e.g. "Your chart benefits
most from warm, nurturing influences — mentors, structured learning, and
people who steady you. Avoid letting things get too dry or driven."}

(Birth chart shown for reference, but explained, not just listed:)
- Year of birth: {year_pillar} — {one short plain-language descriptor}
- Month of birth: {month_pillar} — {descriptor}
- Day of birth: {day_pillar} ← **this is your "core self"** ({plain element})
- Hour of birth: {hour_pillar} — {descriptor}

```

Star notation: `★★★★★` / `★★★★☆` / `★★★☆☆` / `★★☆☆☆` (5/4/3/2). No 1-star.
Vary star distribution across categories. Average around 3.5.

## Readability — both Korean AND English output

The user has explicitly said the reading should be understandable. This is binding.

**Forbidden in any output language:**
- Untranslated 명리 jargon: 편관 / 정관 / 정인 / 편재 / 식상 / 비겁 / 살인상생 / 격국 / 용신 / 대운 / 십신 / 일주 / 신강 / 신약 / 중화 / 합·충·형·파·해
- Naked 한자 stems and branches without an English plain descriptor: 戊, 甲, 申, 戌, etc. alone
- Hexagram names in pure 한자 without explanation: 革, 泰, 否, 既濟, etc.
- Symbols without naming the trigram: ☷ ☱ alone
- Phrases like "월령에 통근하여", "지장간 투출", "왕상휴수사", "납음오행", "庚壬戊"

**Required substitutions — describe the MEANING, not the syllables:**

| Don't write | Do write |
|---|---|
| 편관 (Seven Killings) | "pressure energy — the kind that challenges and tests" |
| 정관 | "structure energy — proper authority, recognition, order" |
| 정인 | "nurturing support — mentors, learning, the protective kind of energy" |
| 편재 | "windfall money — unexpected income, side opportunities" |
| 정재 | "steady earned income, stable assets" |
| 식상 | "self-expression — creativity, output, talent showing" |
| 비겁 | "peer energy — friends, rivals, your sense of self among others" |
| 살인상생 | "the pressure-into-strength pattern — when challenges actually build you up" |
| 일간 / 일주 | "your core self" |
| 신강 / 신약 / 중화 | "strong / weak / balanced chart" |
| 격국 | "the main pattern of your chart" |
| 용신 | "what helps you most" / "favorable energy" |
| 대운 | "10-year life period" / "current decade" |
| 진태양시 보정 | (omit — internal detail) |
| 戊 (Yang Earth) | "Earth-type, the steady mountain kind" |
| 甲 (Yang Wood) | "Wood-type, the upright tree kind" |
| 革 hexagram | "the Revolution hexagram (about timely change)" |
| ☷ over ☱ | "Earth above, Lake below — solid ground over open water" |
| 합·충·형·파·해 | "no notable interaction" / "harmony" / "clash" / "friction" |
| 庚 day, 申 month | (omit; just say what energy it brings) |

**The test:** if a friend who has never heard of 사주 reads the output and asks "what does this word mean?" — you've failed. Every term should already be self-explanatory in context.

**Birth chart pillars in the Life Reading section:** show them (people like seeing the actual characters), but always pair with a plain descriptor. Example: "Day of birth: 戊申 — your core self is Earth-type, steady and grounded."

## `quick` mode (no birth)

Skip Life Reading. Today's Fortune uses generic interpretation.

## Variants & commands

- `/destiny` — full two-section reading (auto profile)
- `/destiny today` — only today's fortune
- `/destiny life` — only life reading
- `/destiny reset` — `rm ~/.destiny/profile.json` and re-prompt
- `/destiny show profile` — print stored profile
- `/destiny in korean|japanese|chinese|spanish` — switch language
- `/destiny born YYYY-MM-DD HH:MM <city> <m|f>` — one-off without saving
- `/destiny quick` — generic daily, no personal data

## Tone & content

- **Specific over generic.** Reference the actual energy of today + the user's actual chart shape — but in plain language. "Today's pushy energy meets your grounded nature" not "today's 편관 against your 戊土".
- **Balanced.** Average ~3.5 stars; vary distribution. Never all 5.
- **No doom.** No direct accident/illness/death/breakup predictions. "A day to take it easy on X" is the limit.
- **No disclaimers.** No "just for fun".
- **Total length** ≤ 35 lines. Today section ≤ 15, Life section ≤ 18.
- **Warm tone.** This is fortune-telling, not a database printout.
- **English default.** Switch on signal.

## Common mistakes

- **Including a "Reasoning" or "Sources" or "Stack" section** — REMOVED. Don't bring it back.
- **Dumping raw 한자 / 명리 jargon in any language** — every term must be replaced with plain-language description.
- **Listing the script's data fields raw** ("shishen_today_to_user_day_master: 편관") — translate everything.
- **Blurring today and life** — keep them in separate sections with clear headers.
- **Inventing pillars/hexagrams** — only what the script returns.
- **Asking for birth info when profile exists** — read profile first.
- **Vague claims** ("you'll have ups and downs") — ground every line in the actual chart energy or hexagram message, just describe it in plain words.
- **Identical star counts** — vary it.
- **Defaulting Korean for English requests** — default English.
