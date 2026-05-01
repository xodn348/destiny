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

## Output format — write as PROSE, not bulleted database rows

The reading must feel like something a thoughtful, warm fortune-teller would say to you over tea. Not a database dump. Not a five-line bullet list with star scores. Real sentences that flow into each other, with concrete imagery and grounded specifics.

### Today's Fortune

```
🔮 **Today's Fortune — {date in warm format: English → "Friday, May 1"; Korean → "목요일, 4월 30일"}**

{**Opening paragraph (2–3 sentences):** set the day's mood vividly with
a concrete image or metaphor. "Today feels like X — Y." Mention how the
day's energy specifically touches THIS user (their core nature). Use sensory
or physical language where you can — light, weather, motion, weight.}

{**Body paragraph (4–6 sentences, flowing prose):** weave through what
the day means for relationships, work, money, body — but as connected
thoughts, NOT a bulleted list. Land 1–2 specific concrete nudges where
they fit naturally ("if a friend suggests dinner out, go", "stretch your
shoulders during the 3pm slump"). Use time-of-day texture if it helps
(morning vs afternoon vs evening). Avoid generic "watch out for X".}

(Visual star summary on a single line — for quick reference, not the main reading:)
⭐ {n}/5 · 💕 {n}/5 · 💰 {n}/5 · 💼 {n}/5 · 🌿 {n}/5

**☯ A reading from the I-Ching for this moment**
{**Narrative form, 3–4 sentences.** Don't just dump the judgment line. Set
the scene: "The hexagram that comes up for you right now is **{name}**.
Imagine **{vivid image of the trigrams — e.g. "still water sitting over
a steady fire — heat rising into a calm reservoir"}**." Then translate
the judgment into modern, accessible language with concrete meaning.
Connect the lesson back to today's mood.}

🍀 {number} · 🎨 {color} · 🧭 {direction} · ✨ *"{≤10 words}"*
```

**Star scale:** 2/5 worst possible (no 1/5). Vary distribution — never identical across categories. Average ~3.5.

### Your Life Reading

```
🌌 **Your Life Reading**

{**Character sketch (3–4 sentences as flowing prose):** describe the user
as a person, the way a friend might write about them. Start with a core
image of who they are. Mention how the chart is built — what makes them
resilient, what they're drawn to, what subtle tension lives inside their
nature. NO "Yang Earth balanced". INSTEAD: "You're built like a quiet
mountain — solid, deliberate, the kind of person people steady themselves
against." Then add nuance: their inner contradictions, their strengths
under pressure, what energy lives in their chart that others sense.}

{**Life arc as a story (one connected paragraph, 4–6 sentences):**
narrate the user's life as chapters of a book. "Your twenties were the
years of... The decade you've just stepped into is when... After 45, the
weight of the chart shifts toward..." Make transitions feel earned, not
listed. Name the years and ages. Land it on where they are right now.}

{**Where you are now (2–3 sentences):** zoom into the current 10-year
period with specific texture. What does this decade feel like to live
through? What's its central theme? What's quietly easier or harder
than before?}

{**What helps you most (2–3 sentences):** describe favorable energy
through specific, concrete examples — not as abstract elements. "You
do best with warm, nurturing presences in your life — mentors, structured
learning, a hot meal at the end of the day. Dry, driven, all-edge
environments wear you down faster than you notice."}

**Your birth chart at a glance** *(the actual data, but with each pillar
explained in a single warm phrase — not a debug list):*
- 1992 (year): **{pillar}** — {one phrase like "deep waters reflecting hard metal"}
- 7th lunar month (month): **{pillar}** — {phrase}
- Day of birth: **{pillar}** ← *your core self*, {phrase like "the patient mountain"}
- 4:30 AM (hour): **{pillar}** — {phrase}
```

**Length target:** Today section 18–22 lines. Life section 22–28 lines. Total reading ≤ 50 lines including spacing. Better to be richly written than to fill a quota — but don't be skimpy either.

**Sentence rhythm:**
- Vary sentence length deliberately. Mix short punches with longer flowing ones.
- Avoid the choppy cadence of "X. Y. Z. W." in a row.
- Use commas, em dashes, colons to create breathing room.
- One vivid image per paragraph beats five abstract claims.

**Forbidden writing patterns:**
- Five bullet points each starting with "★★★☆☆ — ..." — feels like a database
- "Today brings X energy. Be careful with Y. Watch your Z." — flat, generic
- Listing the chart pillars without descriptors
- Repeating the same sentence structure in consecutive lines
- Starting every line with the same word
- Generic platitudes ("balance is important", "trust yourself")

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
- `/destiny compat <partner birth as ISO> <partner city> <partner m|f>` — couple compatibility (궁합) reading using two charts
- `/destiny hook on` — install a Claude Code SessionStart hook so `/destiny` auto-runs each new session
- `/destiny hook off` — remove the destiny SessionStart hook (other hooks preserved)

## /destiny compat — couple compatibility (궁합)

When the user invokes `/destiny compat <partner-info>`:

1. Resolve the user's own profile from `~/.destiny/profile.json` (already saved).
2. Parse the partner's info from the command. Required: birth date+time. Optional: city (→ longitude lookup table above), gender. Defaults if missing: longitude 126.9784 (Seoul), gender `f`, sect 2.
3. Run the script in compat mode:
   ```bash
   python3 "$CLAUDE_PLUGIN_ROOT/skills/destiny/scripts/reading.py" \
     --birth "<user birth>" --lon <user lon> --gender <user g> --sect 2 \
     --partner-birth "<partner birth>" --partner-lon <partner lon> --partner-gender <partner g> --partner-sect 2 \
     --compat
   ```
4. Output sections (in this order, prose-rich, no jargon — same readability rules as the daily reading):

```
💞 **Compatibility reading — {your name or "you"} × {partner name or "your partner"}**

{**Opening (2–3 sentences):** name the core dynamic of the pair using one
vivid image. "You're the patient mountain; they're the moving river — you
hold shape, they reshape what passes through you." Reference both day
masters in plain language, no bare 한자.}

**How you see each other** *(2–3 sentences):* describe what each person
brings to the other, derived from the reciprocal Ten Gods relationship in
the script's `compat.day_master_interaction`. Translate every term into
plain language ("they show up in your life as a steadying authority — the
kind that helps you focus rather than the kind that pressures you").

**Where you run together easily** *(2–3 sentences):* describe the harmonies
the script returned (year-branch and day-branch interactions marked
favorable, plus element-complement signals). Concrete examples — what
this feels like in daily life.

**Where you'll need to translate for each other** *(2–3 sentences):*
describe the friction signals — clashes, doubled-dominant elements,
mismatched element distributions. Frame as differences to navigate,
NOT as compatibility verdicts. Never tell people to break up. Never
predict the relationship's outcome.

**The shape of you together** *(2–3 sentences):* close with the overall
feel — what kind of pair you make, what you're best at as a unit, what
you'll ask of each other to keep growing.
```

**Forbidden in compat readings:**
- "You shouldn't be together" / "this won't work" / any breakup-predicting language
- Numerical "compatibility scores" (e.g. "78% match") — too reductive, classical 궁합 doesn't work that way
- Interpreting the chart as fate. Frame as patterns and tendencies, never as locked outcomes.
- Same readability rules apply: no untranslated 명리 jargon, no bare 한자.

## /destiny hook — auto-run on Claude Code start

**Opt-in only.** Don't suggest this proactively to users — only execute when they invoke `/destiny hook on`.

### `hook on`

```bash
SETTINGS=~/.claude/settings.json
mkdir -p ~/.claude
[ -f "$SETTINGS" ] || echo '{}' > "$SETTINGS"
cp "$SETTINGS" "${SETTINGS}.destiny-backup"
python3 -c "
import json, pathlib
p = pathlib.Path.home() / '.claude' / 'settings.json'
data = json.loads(p.read_text() or '{}')
hooks = data.setdefault('hooks', {})
session_start = hooks.setdefault('SessionStart', [])
existing = [h for h in session_start if h.get('_destiny') is True]
if not existing:
    session_start.append({
        '_destiny': True,
        'matcher': '*',
        'hooks': [{'type': 'command', 'command': \"claude --print '/destiny'\"}]
    })
    p.write_text(json.dumps(data, indent=2))
    print('Installed destiny SessionStart hook. Backup saved to ~/.claude/settings.json.destiny-backup')
else:
    print('destiny SessionStart hook already installed.')
"
```

Then tell the user: "Done. Every new Claude Code session will now auto-run `/destiny`. Disable with `/destiny hook off`."

### `hook off`

```bash
python3 -c "
import json, pathlib
p = pathlib.Path.home() / '.claude' / 'settings.json'
if not p.exists():
    print('No settings file — nothing to remove.')
    raise SystemExit
data = json.loads(p.read_text() or '{}')
hooks = data.get('hooks', {})
session_start = hooks.get('SessionStart', [])
before = len(session_start)
hooks['SessionStart'] = [h for h in session_start if not h.get('_destiny')]
if not hooks['SessionStart']:
    hooks.pop('SessionStart', None)
if not hooks:
    data.pop('hooks', None)
p.write_text(json.dumps(data, indent=2))
removed = before - len(hooks.get('SessionStart', []))
print(f'Removed {removed} destiny hook(s). Other hooks preserved.')
"
```

### Safety rules

- Always create `~/.claude/settings.json.destiny-backup` before modifying on `hook on`
- Identify destiny-installed hooks by the `_destiny: true` marker so removal never touches the user's other hooks
- Never enable the hook without explicit user invocation of `/destiny hook on`

## Tone & content

- **Specific over generic.** Reference the actual energy of today + the user's actual chart shape — but in plain language. "Today's pushy energy meets your grounded nature" not "today's 편관 against your 戊土".
- **Balanced.** Average ~3.5 stars; vary distribution. Never all 5.
- **No doom.** No direct accident/illness/death/breakup predictions. "A day to take it easy on X" is the limit.
- **No disclaimers.** No "just for fun".
- **Length: rich prose, not data printout.** Today section 18–22 lines. Life section 22–28 lines. Trade quantity of bullets for quality of sentences.
- **Warm, embodied tone.** This is a fortune-teller speaking — sensory, image-driven, alive. Not a database printout. Not corporate copy.
- **Concrete over abstract.** "Stretch during the 3pm slump" beats "watch your health". A vivid image of still water over fire beats "Hexagram 49: Revolution".
- **English default.** Switch on signal.

## Anchor example — what good output looks like

This is the format and quality bar (English, real /destiny run, profile = 1992-07-31 04:30 Suwon m, on 2026-05-01). Use it as a reference for tone, paragraph length, sensory imagery, the single-line stars row, the narrative I-Ching paragraph, and the birth-chart-pillars table. **Do not copy the prose verbatim — generate fresh prose for the actual user/day, but match the shape.**

```
🔮 **Today's Fortune — Friday, May 1**

Today moves like a soft rain that arrives after weeks of dry wind — quiet, intelligent,
soaking in slowly instead of pouring all at once. That softness lands on your steady,
mountain-like nature and unlocks something the noisier days couldn't reach: people
noticing what you've already built, and naming it out loud.

The energy around you carries a friendly kind of authority — the structure-and-order
kind, not the pressure kind. A manager catching the prep work you did last week, a
client returning a message at exactly the right moment, a quiet confirmation from
someone whose opinion actually matters: all the same texture. Mid-morning is when
this is most alive; the late afternoon is for digesting it without rushing the next
move. Money holds steady but doesn't spike — don't reach for the windfall today,
hold the line. If your shoulders tighten by 3pm, that's the day asking you to
stretch, not push through.

⭐ 4/5 · 💕 3/5 · 💰 3/5 · 💼 5/5 · 🌿 4/5

**☯ A reading from the I-Ching for this moment**
The hexagram that comes up for you right now is **Biting Through**. Picture flames
flickering above thunder — bright, decisive light sitting on top of a deep rumble
that's been waiting to break. There is something stuck between you and the next
clean step, and the old wisdom is unusually direct: don't work around it, name it,
let the small moment of friction do its work. The moving line is the very last one
— the window is today.

🍀 16 · 🎨 warm ochre · 🧭 center · ✨ *"name the obstruction by sundown."*

---

🌌 **Your Life Reading**

You are built like a wide, low mountain at the edge of an old forest — the kind of
mountain people don't notice from far away, but lean against the moment they get
close. Solid, warm, rock that cooled slowly enough to keep its shape through any
weather. There's a quiet sharpness inside you, though: hidden seams of metal running
through patient earth, an inner edge that cuts away whatever doesn't serve. Your
chart is unusually balanced — wood, fire, earth, metal, water all present, none
drowning the others — which means you can hold contradictory things without breaking.

Your twenties were the years of patient layering — quietly accumulating skills,
relationships, and a sense of your own shape, while from the outside it looked like
nothing dramatic was happening. The decade you've just stepped into, from age 34
through 43, is when that buried work surfaces. The chart shifts from "taking in" to
"giving off" — what you've made starts speaking for itself. Less proving, more
publishing. After 44 the rhythm slows again, into a deeper kind of authority.

This decade feels lighter than the one before it, even when the work is harder.
Things that used to require explanation just land. The central theme is going
public with something — a body of work, a stance, a direction — and discovering
people were already waiting for it.

You do best with structured environments that have warmth in them — long-running
projects, a consistent home, mentors who teach by example rather than lecture, food
that takes time to cook. Cold, transactional, all-edge places will wear you down
faster than you notice.

**Your birth chart at a glance:**
- 1992 (year): **壬申** — deep waters running over hard mountain metal
- 7th lunar month: **丁未** — a small flame inside late-summer earth
- Day of birth: **戊申** ← *your core self*, the patient mountain with veins of metal
- 4:30 AM (hour): **甲寅** — a tall tree in deep forest at first light
```

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
