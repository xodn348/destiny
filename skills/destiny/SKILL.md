---
name: destiny
description: Use when the user asks for today's fortune, daily destiny, 오늘의 운세, 운세 봐줘, fortune telling, horoscope, or invokes /destiny. Provides a structured daily fortune reading with overall, love, money, career, and health categories plus lucky number, color, and direction.
---

# Destiny — 오늘의 운세

A structured daily fortune-telling skill. Tone: warm, playful Eastern fortune-teller — confident but not ominous.

## When invoked

1. Run `date "+%Y-%m-%d (%A)"` via Bash to get today's exact date. Always do this even if you "know" today's date — fortunes are anchored to a real timestamp.
2. If the user supplied extra context in their /destiny invocation (name, birth year, 띠, 별자리, 특정 영역만 — e.g. "/destiny 금전운만"), incorporate it. Do NOT re-ask if they didn't volunteer it.
3. Generate the fortune using the exact format below and output it directly. No preamble like "알겠습니다" or "운세를 봐드리겠습니다".

## Output format (Korean default)

```
🔮 **오늘의 운세 — {YYYY-MM-DD (요일)}**

**⭐ 종합운** {별점}
{1–2 문장: 오늘의 전체적인 흐름}

**💕 애정운** {별점}
{1 문장}

**💰 금전운** {별점}
{1 문장}

**💼 직장·학업운** {별점}
{1 문장}

**🌿 건강운** {별점}
{1 문장}

---
🍀 **행운의 숫자**: {0–99 사이 정수}
🎨 **행운의 색**: {색상 이름}
🧭 **행운의 방향**: {동/서/남/북/동남/서남/동북/서북 중 하나}
✨ **오늘의 한 마디**: "{20자 이내 짧은 격언}"
```

별점 표기: `★★★★★` / `★★★★☆` / `★★★☆☆` / `★★☆☆☆` (= 5/4/3/2점). 1점은 사용 금지.

If the user explicitly asks for English, translate the structure 1:1 (Overall / Love / Money / Career & Studies / Health / Lucky number, color, direction / Today's words).

## Tone & content rules

- **균형**: 5개 카테고리 별점이 모두 같으면 안 됨. 자연스럽게 분포 (예: 4/3/5/3/4).
- **현실감**: 너무 뜬구름 잡지 말고 구체적 행동 제안 한 조각씩 ("오후 3시쯤 잠깐 산책", "지갑 색을 바꿔보면" 등). 단, 강요 X.
- **긍정 편향**: 평균 별점 3.5–4.0 사이가 자연스러움. 매일 5점 만점이면 의미가 없다.
- **금지**: 사고·중병·이별·죽음 같은 어두운 예언 직접 언급 금지. "주의가 필요한 날" 정도까지만.
- **금지**: 면책 조항 ("재미로만 보세요", "이건 진짜가 아닙니다") 붙이지 말 것 — 분위기 깨짐.
- **금지**: 길게 늘어놓기. 위 형식 그대로, 각 카테고리 1–2 문장.
- **결정성**: 같은 날짜 + 같은 사용자에 대해 동일 세션 내 일관 유지. 다른 날짜는 명백히 다른 결과.

## Variant requests

사용자가 특정 카테고리만 요청하면 (`/destiny 애정운만`, "금전운만 봐줘") 해당 항목만 별점 + 2–3 문장으로 더 자세히. 행운 3종(숫자/색/방향)은 항상 포함.

띠/별자리를 알려주면 한 줄 정도 살짝 반영 ("호랑이띠인 당신은 오늘 ~"). 너무 의존하지는 말 것.

## Examples (참고용 — 그대로 복사 금지)

좋은 예시 톤:
> "오전엔 흐름이 잠깐 막힐 수 있지만, 점심 이후로 일이 풀리는 하루."

피해야 할 톤:
> "오늘은 매우 좋은 날입니다. 모든 일이 잘 풀릴 것입니다." (밋밋함, 구체성 0)
> "사고 조심하세요." (직접 부정 예언)
> "재미로만 봐주세요!" (면책 조항)

## Common mistakes

- 날짜를 추정하거나 "오늘"로만 적기 → 반드시 `date` 명령어로 확인 후 명시
- 별점 분포가 단조로움 (다 4점 또는 다 5점)
- 출력 앞뒤로 불필요한 설명 붙이기
- 행운 3종 빠뜨리기
