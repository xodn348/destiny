# destiny

오늘의 운세 (daily fortune) skill for [Claude Code](https://claude.com/claude-code).

Invoke `/destiny` and get a structured daily fortune — 종합운, 애정운, 금전운, 직장·학업운, 건강운 — plus a lucky number, color, and direction.

```
🔮 오늘의 운세 — 2026-04-30 (Thursday)

⭐ 종합운 ★★★★☆
오전엔 흐름이 잠깐 막힐 수 있지만, 점심 이후로 일이 풀리는 하루.

💕 애정운 ★★★☆☆
가까운 사람의 작은 말 한 마디에 의미를 두지 마세요.

💰 금전운 ★★★★☆
예상치 못한 환급이나 작은 보너스가 들어올 수 있어요.

💼 직장·학업운 ★★★★★
오후 3시 전후로 막혔던 문제의 실마리가 풀립니다.

🌿 건강운 ★★★☆☆
어깨와 목이 굳기 쉬운 날 — 짧게라도 스트레칭을.

---
🍀 행운의 숫자: 27
🎨 행운의 색: 짙은 청록
🧭 행운의 방향: 동남
✨ 오늘의 한 마디: "급할수록 천천히"
```

## Install

This repo is both a Claude Code **plugin** and a single-plugin **marketplace**. Add it as a marketplace, then install the plugin:

```
/plugin marketplace add xodn348/destiny
/plugin install destiny@destiny-marketplace
```

(Or after cloning locally: `/plugin marketplace add ~/code/destiny`.)

## Use

```
/destiny
```

Variants:
- `/destiny 애정운만` — 한 카테고리만 자세히
- `/destiny 호랑이띠 1992년생` — 띠/생년 반영
- `/destiny in english` — English output

## License

MIT
