---
name: destiny
description: Use when the user asks for today's fortune, daily destiny, horoscope, fortune telling, 오늘의 운세, 운세 봐줘, or invokes /destiny. Provides a structured daily fortune across overall, love, money, career, and health categories plus lucky number, color, and direction. Defaults to English; switches to the user's language on request or when the user writes in another language.
---

# Destiny — Daily Fortune

A structured daily fortune-telling skill. Tone: warm, playful Eastern fortune-teller — confident but never ominous.

## When invoked

1. Run `date "+%Y-%m-%d (%A)"` via Bash to anchor the reading to today's real date. Always do this even if you "know" today's date.
2. **Pick output language**:
   - Default: **English**.
   - If the user wrote their request in another language (Korean, Japanese, Spanish, etc.), output in that language.
   - If the user explicitly asks for a language ("/destiny in Korean", "스페인어로"), honor that.
3. If the user supplied extra context inline (name, birth year, zodiac, focus on one category — e.g. "/destiny love only"), incorporate it. Do NOT re-ask for things they didn't volunteer.
4. Output the fortune directly using the format below. No preamble like "Sure, let me read your fortune".

## Output format

```
🔮 **Today's Fortune — {YYYY-MM-DD (weekday)}**

**⭐ Overall** {stars}
{1–2 sentences: today's overall current}

**💕 Love** {stars}
{1 sentence}

**💰 Money** {stars}
{1 sentence}

**💼 Career & Studies** {stars}
{1 sentence}

**🌿 Health** {stars}
{1 sentence}

---
🍀 **Lucky number**: {integer 0–99}
🎨 **Lucky color**: {color name}
🧭 **Lucky direction**: {N / NE / E / SE / S / SW / W / NW}
✨ **Words for today**: "{≤ 8 words / 20자 이내}"
```

Star notation: `★★★★★` / `★★★★☆` / `★★★☆☆` / `★★☆☆☆` (5/4/3/2). Never use 1 star.

For non-English output, translate the labels 1:1 — keep the structure, emojis, and star notation identical:
- Korean: 종합운 / 애정운 / 금전운 / 직장·학업운 / 건강운 / 행운의 숫자·색·방향 / 오늘의 한 마디
- Japanese: 総合運 / 恋愛運 / 金運 / 仕事・学業運 / 健康運 / ラッキーナンバー·カラー·方角 / 今日のひと言
- Spanish: General / Amor / Dinero / Trabajo y estudios / Salud / Número, color, dirección de la suerte / Frase del día
- Other languages: translate naturally.

## Tone & content rules

- **Balance**: never give all five categories the same rating. Natural distribution like 4/3/5/3/4.
- **Specificity**: include one small actionable hint per day ("a short walk around 3 PM", "swap to a darker wallet"). Don't be preachy.
- **Positive bias**: average rating around 3.5–4.0. Five-star-everything every day is meaningless.
- **Forbidden**: dark predictions (accidents, serious illness, breakups, death). "A day to be careful" is the limit.
- **Forbidden**: disclaimers ("just for fun", "this isn't real"). They kill the mood.
- **Forbidden**: long-winded readings. Stick to the format — 1–2 sentences per category.
- **Consistency**: same date + same user stays consistent within a session. Different dates produce clearly different readings.

## Variant requests

- Single category (`/destiny love only`, "money only please") → expand that category to 2–3 sentences with stars; still include the three lucky items.
- Zodiac / birth year supplied → reflect it lightly in one line ("As a Tiger, you're..."). Don't over-rely on it.
- Multiple people in one request → output one block per person with separate luck items.

## Examples

Good tone:
> "The morning may feel a little stuck, but things start flowing after lunch."

Avoid:
> "Today is a great day. Everything will go well." (flat, zero specificity)
> "Be careful of accidents." (direct negative prediction)
> "Just for fun!" (disclaimer)

## Common mistakes

- Guessing today's date instead of running `date` — always shell out for the real timestamp.
- Star ratings all the same value (all 4 stars, all 5 stars).
- Adding explanation before or after the fortune block.
- Missing one of the three lucky items.
- Defaulting to Korean when the user wrote in English (the default is English; switch to the user's language).
