---
name: destiny
description: Use when the user asks for a fortune reading, daily destiny, life reading, horoscope, hexagram, I-Ching, 운세, 사주, 명리, or invokes /destiny. Produces THREE sections in one reading — (1) today's daily fortune, (2) full life destiny analysis from the user's 사주, (3) reasoning footnotes that explain what data and 명리 logic backed each conclusion. Computes real 사주 + 일진 + 매화역수 hexagram via lunar-python, then Claude applies its 명리 knowledge to interpret. Stores birth profile after first use. Default English.
---

# Destiny — Today + Life Reading + Reasoning

`/destiny` produces a complete reading in three sections, in this order:

1. **🔮 Today's Fortune** — daily 5-category stars + hexagram
2. **🌌 Life Destiny** — character, life arc, current 대운, key themes from the full 사주
3. **📚 Reasoning** — what data and 명리 logic produced each conclusion (transparent footnotes)

The point of section 3 is honesty: every claim above should be traceable to either (a) the script's deterministic output or (b) a specific 명리 principle Claude is applying. No mystery, no "trust me."

## Iron rules

- **Never invent stems, branches, hexagrams, or interaction labels.** Only use what the script returns.
- **Always include the Reasoning section.** It's not optional. It's what makes this skill different from a horoscope.
- **Distinguish today vs life clearly** — never blur them. Today's section talks about today only. Life section talks about lifelong patterns.

## Workflow

### Step 1 — check for stored profile

```bash
PROFILE=~/.destiny/profile.json
[ -f "$PROFILE" ] && cat "$PROFILE"
```

Profile exists → skip to Step 3.

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
| Busan | 129.08 | Osaka | 135.50 |
| Jeju | 126.52 | Beijing | 116.41 |
| New York | -74.01 | London | -0.13 |
| LA | -118.24 | Paris | 2.35 |
| Sydney | 151.21 | Singapore | 103.82 |

### Step 3 — run script

```bash
python3 -m pip install --quiet lunar-python 2>/dev/null
python3 "$CLAUDE_PLUGIN_ROOT/skills/destiny/scripts/reading.py" \
    --birth "<birth>" --lon <lon> --gender <gender> --sect <sect>
```

JSON returned:
- `today` — date, day pillar, day element
- `personal` — pillars, day_master, **chart_summary** (element count, season, day master strength, missing/dominant elements), da_yun (8 cycles)
- `interaction` — 십신 of today→user-day-master + branch relation, with metadata
- `iching` — hexagram via 매화역수
- `lucky` — number/color/direction (computed)

### Step 4 — write the three-section reading

## Output format (English default)

```
🔮 **Today's Fortune — {date}**

Today is **{today_day_pillar} day** ({today.day_element}). Against your
{user_day_pillar} day master, today brings **{shishen}** energy.
{1 line: branch relation if 합/충/형, skip if 무관계.}

**⭐ Overall** {stars}      {1 line, today only}
**💕 Love** {stars}         {1 line}
**💰 Money** {stars}        {1 line}
**💼 Career** {stars}       {1 line}
**🌿 Health** {stars}       {1 line}

**☯ Hexagram for this moment**
{num}. {en} ({ko} · {zh}) — moving line {moving_line}
{upper_symbol} over {lower_symbol}
"{judgment}"
{1–2 sentences applying to TODAY only.}

🍀 Lucky number: {n}    🎨 {color}    🧭 {direction}
✨ "{≤8 words}"

---

🌌 **Your Life Destiny (전체 운명)**

**Birth chart (사주팔자)**
- Year   {year.gz} ({ko}, {nayin})
- Month  {month.gz} ({ko}, {nayin}) ← Month branch {month_branch} = {season_of_birth}
- Day    {day.gz} ({ko}, {nayin}) ← **Day master {day_master} ({day_master_element}, {polarity}, {strength})**
- Hour   {hour.gz} ({ko}, {nayin})

Element distribution: 木{Wood} 火{Fire} 土{Earth} 金{Metal} 水{Water}
Dominant: {dominant_element} · Missing: {missing_elements joined or "none"}

**Character (성향)**
{2–3 sentences. Use day master + element distribution + dominant 십신 (year_gan/month_gan from saju.shishen).
Apply your 명리 knowledge — this is a lifelong character read, not today.
Anchor every claim to a specific element or 십신 you can name.}

**Life arc (인생 흐름)**
{2–3 sentences walking through the 대운 cycles — early life (first 1–2 cycles),
mid-life (3rd–5th cycles), later life (6th+). Note transitions where the
ganzhi element of the cycle shifts dramatically.}

**Current 10-year cycle**
{Find the da_yun whose start_year ≤ today's year < next start_year.}
{ganzhi} ({ko}), age {start_age}–{next.start_age - 1}
{2 sentences on the cycle's element vs day master, how it supports or pressures.}

**Estimated 용신 (favorable element)**
{Claude's reasoning. If day master is strong → reduce/drain via 식상/재성/관성.
If weak → support via 인성/비겁. Name the element + give 1 sentence why.}

**Estimated 격국 (chart structure)**
{Claude's best guess: 정관격, 식신격, 편재격, 종왕격, etc., based on month branch
and dominant 십신. 1 sentence why.}

---

📚 **Reasoning (근거)**

**Today's stars — what determined them:**
- The shishen of today's day stem ({today.day_gan}) against your day master ({day_master}) is **{shishen}**, which classical 명리 associates with {shishen_meta.domains joined}. Tendency: {shishen_meta.tendency}.
- Branch relation between today's {today.day_zhi} and your {user_day_zhi}: {branch_relation}. Tendency: {branch_meta.tendency}.
- {Each star score gets 1 short justification: e.g. "Money 4★ — 편재 favors windfall income, but no 삼합 to amplify"}.

**Life-reading sources:**
- Day master strength estimate ({strength}) is from element distribution: {supportive_count_for_day_master} of 8 chars support your {day_master_element} self. Refined by 월령 ({month_branch} = {season_dominant_element} season).
- Character read draws on {day_master_element} day master archetype + dominant {dominant_element} influence + month-stem 십신 ({saju.shishen.month_gan}).
- 용신 reasoning: {brief — strong/weak day master + missing/excess elements + season}.
- 격국 reasoning: {brief — month branch hidden stem + transparent stem in chart}.
- 대운 transitions are deterministic from birth (gender + year stem polarity → forward/backward cycle).

**Hexagram method:**
- 매화역수 시점법 — lunar 연(year branch index {y}) + 월({m}) + 일({d}) [+ user salt {salt}] → upper trigram. + 시({h}) → lower trigram. Sum mod 6 → moving line. Hexagram lookup from King Wen ordering, judgment text from James Legge (1899).

**Stack:**
- 사주 8 chars: lunar-python (real 만세력) with true-solar-time correction ({offset_min} min for longitude {lon}), DST adjustment, 야자시 rule.
- 십신 + 합충형: classical 60갑자 lookup tables in script.
- Star judgments + character reading + 용신/격국 estimates: Claude applying 명리 knowledge from training data (자평진전, 적천수, modern 명리 references) — not a hand-tuned numeric table.
- Daily randomness: zero. Same person + same date = same script output. The prose differs each call (LLM generation).

**What's NOT in the reading:**
- 신살(神煞) detailed lookup, hidden stems (지장간) per branch, 12운성, 공망, 세운(year cycle) interaction. These can be added with deeper script support; current reading uses high-level 십신 + 합충 only.
```

Star notation: `★★★★★` / `★★★★☆` / `★★★☆☆` / `★★☆☆☆` (5/4/3/2). No 1-star.

## `quick` mode (no birth)

If user chose `quick`: skip Life Destiny section. Today's Fortune uses generic interpretation. Reasoning section explains it's a generic reading and how to upgrade.

## Variants & commands

- `/destiny` — full three-section reading (auto profile)
- `/destiny today` — only today's fortune section
- `/destiny life` — only life destiny section
- `/destiny reset` — `rm ~/.destiny/profile.json` and re-prompt
- `/destiny show profile` — print stored profile
- `/destiny in korean|japanese|chinese|spanish` — switch language
- `/destiny born YYYY-MM-DD HH:MM <city> <m|f>` — one-off without saving
- `/destiny quick` — generic daily, no personal data

## Tone & content

- **Specific over generic.** Always reference the actual 십신, 일주, hexagram, element. No "you are creative and resilient."
- **Balanced.** Average ~3.5 stars; vary distribution. Never all 5.
- **No doom.** No direct accident/illness/death/breakup predictions. "A day for caution in X" is the limit.
- **No disclaimers.** No "just for fun." The Reasoning section provides the honesty.
- **Total length** ≤ 70 lines. Today section ≤ 18, Life section ≤ 22, Reasoning ≤ 20.
- **English default.** Switch on signal.
- **Foreigner-friendly.** Always provide both 한자 and English/한글 transliteration on first reference of any term.

## Common mistakes

- **Skipping the Reasoning section** — never. It's mandatory.
- **Blurring today and life** — keep them in separate sections with clear headers.
- **Inventing pillars/hexagrams** — only script output.
- **Asking for birth info when profile exists** — read profile first.
- **Vague life claims** ("you'll have ups and downs") — useless. Anchor to specific 십신, element, or 대운 cycle.
- **Identical star counts across categories** — vary it.
- **Defaulting Korean for English requests** — default English.
- **Forgetting `pip install lunar-python`** — run idempotently every call.
