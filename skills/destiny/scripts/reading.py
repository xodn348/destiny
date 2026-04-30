#!/usr/bin/env python3
"""
destiny reading — personalized daily fortune from real 만세력 + 십신 + 매화역수.

Without --birth: minimal daily reading (same for everyone that day) —
hexagram + today's day pillar + generic lucky items.

With --birth (recommended path):
  - Real Four Pillars chart with 진태양시 / DST / 야자시 corrections
  - Today × user analysis: 십신 of today's day stem to user's day master,
    plus branch relation (삼합/육합/충/형) of today's day branch to user's
  - Five-category scores (overall/love/money/career/health, 2–5) computed
    from the above relationship — different for every birth chart
  - Lucky color/direction matched to the user's day master element
  - One I-Ching hexagram via 매화역수 시점법

Outputs JSON. Claude interprets the structured numbers into a reading.
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timedelta
from pathlib import Path

try:
    from lunar_python import Solar
except ImportError:
    print(json.dumps({
        "error": "lunar-python not installed",
        "fix": "python3 -m pip install lunar-python",
    }, ensure_ascii=False))
    sys.exit(2)

KST_STANDARD_LON = 135.0
SEOUL_LON = 126.9784

GAN_KO = {"甲":"갑","乙":"을","丙":"병","丁":"정","戊":"무",
          "己":"기","庚":"경","辛":"신","壬":"임","癸":"계"}
ZHI_KO = {"子":"자","丑":"축","寅":"인","卯":"묘","辰":"진","巳":"사",
          "午":"오","未":"미","申":"신","酉":"유","戌":"술","亥":"해"}
ZHI_LIST = ["子","丑","寅","卯","辰","巳","午","未","申","酉","戌","亥"]
GAN_ELEMENT = {
    "甲":("Wood","yang"),"乙":("Wood","yin"),
    "丙":("Fire","yang"),"丁":("Fire","yin"),
    "戊":("Earth","yang"),"己":("Earth","yin"),
    "庚":("Metal","yang"),"辛":("Metal","yin"),
    "壬":("Water","yang"),"癸":("Water","yin"),
}
ELEMENT_GENERATES = {"Wood":"Fire","Fire":"Earth","Earth":"Metal","Metal":"Water","Water":"Wood"}
ELEMENT_CONTROLS  = {"Wood":"Earth","Earth":"Water","Water":"Fire","Fire":"Metal","Metal":"Wood"}
ELEMENT_COLOR = {
    "Wood":  "Forest green",
    "Fire":  "Crimson red",
    "Earth": "Warm ochre",
    "Metal": "Pearl white",
    "Water": "Deep indigo",
}
ELEMENT_DIRECTION = {
    "Wood":"East","Fire":"South","Earth":"Center","Metal":"West","Water":"North",
}
TRIGRAM = {
    1:("乾","Heaven","☰"), 2:("兌","Lake","☱"),
    3:("離","Fire","☲"),   4:("震","Thunder","☳"),
    5:("巽","Wind","☴"),   6:("坎","Water","☵"),
    7:("艮","Mountain","☶"), 8:("坤","Earth","☷"),
}

# Ten Gods metadata — domains and watch-areas from classical 명리 通說
# (자평진전, 적천수). NO numeric scores: Claude judges intensity/stars
# from this metadata + chart context using its 명리 knowledge.
SHISHEN_META = {
    "비견": {
        "en": "Companion — peer of same kind",
        "domains": ["self-confidence", "friendship", "independence", "siblings"],
        "watch":   ["stubbornness", "over-competition with peers"],
        "tendency": "neutral",
    },
    "겁재": {
        "en": "Rival — peer-competitor",
        "domains": ["bold action", "social risk", "spending"],
        "watch":   ["money loss", "rivalry", "impulsive choices"],
        "tendency": "challenging",
    },
    "식신": {
        "en": "Output — gentle expression",
        "domains": ["creativity", "appetite", "ease", "children", "talent"],
        "watch":   ["complacency", "overindulgence"],
        "tendency": "favorable",
    },
    "상관": {
        "en": "Output-rebel — sharp expression",
        "domains": ["self-expression", "wit", "skill-based income"],
        "watch":   ["sharp tongue", "authority conflict", "reputation"],
        "tendency": "mixed",
    },
    "편재": {
        "en": "Side-wealth — windfall money",
        "domains": ["unexpected income", "side business", "social wealth"],
        "watch":   ["scattered focus", "speculative loss"],
        "tendency": "favorable",
    },
    "정재": {
        "en": "Direct-wealth — steady money",
        "domains": ["earned income", "fixed assets", "diligence", "spouse(M)"],
        "watch":   ["over-attachment to material"],
        "tendency": "very favorable",
    },
    "편관": {
        "en": "Pressure — Seven Killings",
        "domains": ["challenge", "discipline", "courage under fire"],
        "watch":   ["stress", "physical strain", "authority pressure"],
        "tendency": "challenging",
    },
    "정관": {
        "en": "Authority — proper order",
        "domains": ["career advancement", "honor", "structure", "spouse(F)"],
        "watch":   ["over-formality", "rigid scheduling"],
        "tendency": "favorable",
    },
    "편인": {
        "en": "Side-resource — unconventional support",
        "domains": ["intuition", "lateral learning", "spirituality"],
        "watch":   ["isolation", "overthinking", "appetite drop"],
        "tendency": "mixed",
    },
    "정인": {
        "en": "Direct-resource — proper support",
        "domains": ["learning", "documents", "mentorship", "calm health", "mother"],
        "watch":   ["over-reliance on others"],
        "tendency": "very favorable",
    },
}

BRANCH_META = {
    "비화":   {"tendency": "neutral",         "note": "same branch — quiet resonance, day reinforces your nature"},
    "삼합":   {"tendency": "very favorable",  "note": "Three-Harmony alignment — strong supportive flow across domains"},
    "육합":   {"tendency": "favorable",       "note": "Six-Union — gentle compatibility, smooth interactions"},
    "충":     {"tendency": "challenging",     "note": "Direct clash — turbulence, forced change, decisions made for you"},
    "형":     {"tendency": "challenging",     "note": "Punishment — friction, things grind, irritations multiply"},
    "무관계": {"tendency": "neutral",         "note": "no major branch interaction today"},
}

SAN_HE = [("申","子","辰"), ("亥","卯","未"), ("寅","午","戌"), ("巳","酉","丑")]
LIU_HE = {frozenset({"子","丑"}), frozenset({"寅","亥"}), frozenset({"卯","戌"}),
          frozenset({"辰","酉"}), frozenset({"巳","申"}), frozenset({"午","未"})}
LIU_CHONG = {frozenset({"子","午"}), frozenset({"丑","未"}), frozenset({"寅","申"}),
             frozenset({"卯","酉"}), frozenset({"辰","戌"}), frozenset({"巳","亥"})}
SAN_XING = [("寅","巳","申"), ("丑","戌","未")]
XIANG_XING = {frozenset({"子","卯"})}


def korean_dst(dt: datetime) -> bool:
    return datetime(1987, 5, 10, 2, 0) <= dt < datetime(1988, 10, 9, 3, 0)

def true_solar_offset_minutes(longitude: float) -> int:
    return round((longitude - KST_STANDARD_LON) * 4)

def gz_to_ko(gz: str) -> str:
    return GAN_KO.get(gz[0], gz[0]) + ZHI_KO.get(gz[1], gz[1]) if len(gz) == 2 else gz


def shishen_of(other_gan: str, day_gan: str) -> str:
    other_el, other_pol = GAN_ELEMENT[other_gan]
    self_el,  self_pol  = GAN_ELEMENT[day_gan]
    same = (other_pol == self_pol)
    if other_el == self_el:
        return "비견" if same else "겁재"
    if ELEMENT_GENERATES[self_el] == other_el:
        return "식신" if same else "상관"
    if ELEMENT_CONTROLS[self_el] == other_el:
        return "편재" if same else "정재"
    if ELEMENT_CONTROLS[other_el] == self_el:
        return "편관" if same else "정관"
    if ELEMENT_GENERATES[other_el] == self_el:
        return "편인" if same else "정인"
    return "?"


def branch_relation(today_zhi: str, user_zhi: str) -> str:
    if today_zhi == user_zhi:
        return "비화"
    pair = frozenset({today_zhi, user_zhi})
    for triplet in SAN_HE:
        if today_zhi in triplet and user_zhi in triplet:
            return "삼합"
    if pair in LIU_HE:
        return "육합"
    if pair in LIU_CHONG:
        return "충"
    for triplet in SAN_XING:
        if today_zhi in triplet and user_zhi in triplet:
            return "형"
    if pair in XIANG_XING:
        return "형"
    return "무관계"


def saju(birth_clock: datetime, longitude: float, sect: int, gender: str, time_unknown: bool):
    dst = korean_dst(birth_clock)
    after_dst = birth_clock - timedelta(hours=1) if dst else birth_clock
    offset_min = true_solar_offset_minutes(longitude)
    corrected = after_dst + timedelta(minutes=offset_min)

    s = Solar.fromYmdHms(corrected.year, corrected.month, corrected.day,
                         corrected.hour, corrected.minute, corrected.second)
    lunar = s.getLunar()
    ec = lunar.getEightChar()
    ec.setSect(sect)

    pillars = {
        "year":  {"gz": ec.getYear(),  "ko": gz_to_ko(ec.getYear()),  "nayin": ec.getYearNaYin()},
        "month": {"gz": ec.getMonth(), "ko": gz_to_ko(ec.getMonth()), "nayin": ec.getMonthNaYin()},
        "day":   {"gz": ec.getDay(),   "ko": gz_to_ko(ec.getDay()),   "nayin": ec.getDayNaYin()},
    }
    if time_unknown:
        pillars["hour"] = {"gz": "?", "ko": "?", "nayin": "?", "note": "birth time unknown"}
    else:
        pillars["hour"] = {"gz": ec.getTime(), "ko": gz_to_ko(ec.getTime()), "nayin": ec.getTimeNaYin()}

    da_yun = []
    try:
        for d in ec.getYun(1 if gender == "m" else 0).getDaYun()[:8]:
            gz = d.getGanZhi()
            da_yun.append({
                "start_year": d.getStartYear(),
                "start_age":  d.getStartAge(),
                "ganzhi":     gz,
                "ganzhi_ko":  gz_to_ko(gz),
            })
    except Exception:
        pass

    day_gan = pillars["day"]["gz"][0]
    return {
        "input": {
            "birth_clock_local": birth_clock.isoformat(),
            "longitude": longitude,
            "sect_rule": "야자시" if sect == 2 else "조자시",
            "dst_applied": dst,
            "true_solar_offset_minutes": offset_min,
            "corrected_for_calculation": corrected.isoformat(),
            "lunar_birth": f"{lunar.getYearInChinese()}년 {lunar.getMonthInChinese()}월 {lunar.getDayInChinese()}일",
            "gender": gender,
            "time_unknown": time_unknown,
        },
        "pillars": pillars,
        "day_master": day_gan,
        "day_master_element": GAN_ELEMENT[day_gan][0],
        "day_master_polarity": GAN_ELEMENT[day_gan][1],
        "da_yun": da_yun,
    }


def today_block(now: datetime):
    s = Solar.fromYmdHms(now.year, now.month, now.day, now.hour, now.minute, 0)
    l = s.getLunar()
    return {
        "date": now.strftime("%Y-%m-%d %A"),
        "year_pillar":  l.getYearInGanZhi(),
        "month_pillar": l.getMonthInGanZhi(),
        "day_pillar":   l.getDayInGanZhi(),
        "day_gan":      l.getDayGan(),
        "day_zhi":      l.getDayZhi(),
        "day_element":  GAN_ELEMENT[l.getDayGan()][0],
        "lunar_date":   f"{l.getYearInChinese()}년 {l.getMonthInChinese()}월 {l.getDayInChinese()}일",
    }


def iching_meihua(now: datetime, hex_data: dict, salt: int = 0) -> dict:
    """매화역수 시점법. salt로 사용자별 약간의 변주를 줘서 같은 시각에도 사람마다 괘가 달라지게."""
    s = Solar.fromYmdHms(now.year, now.month, now.day, now.hour, now.minute, 0)
    l = s.getLunar()
    y = ZHI_LIST.index(l.getYearZhi()) + 1
    m = abs(l.getMonth())
    d = abs(l.getDay())
    h = ((now.hour + 1) // 2) % 12 + 1
    upper = (y + m + d + salt) % 8 or 8
    total = y + m + d + h + salt
    lower = total % 8 or 8
    moving = total % 6 or 6
    info = hex_data[f"{upper},{lower}"]
    return {
        "method": "매화역수 시점법 (plum-blossom time divination)" + (f" with personal salt={salt}" if salt else ""),
        "upper_trigram": list(TRIGRAM[upper]),
        "lower_trigram": list(TRIGRAM[lower]),
        "moving_line": moving,
        "_total": total,
        **info,
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--birth", help="ISO datetime of birth, local clock at birthplace, e.g. 1992-08-15T14:30")
    p.add_argument("--lon", type=float, default=SEOUL_LON,
                   help="Birthplace longitude in °E. Seoul=126.9784, Tokyo=139.69, NYC=-74.01, London=-0.13")
    p.add_argument("--sect", type=int, default=2, choices=[1, 2],
                   help="Hour-pillar rule: 1=조자시, 2=야자시 (Korean default)")
    p.add_argument("--gender", choices=["m", "f"], default="m")
    p.add_argument("--time-unknown", action="store_true",
                   help="Birth time unknown — skip hour pillar")
    args = p.parse_args()

    now = datetime.now()
    here = Path(__file__).parent
    with open(here / "iching_64.json", encoding="utf-8") as f:
        hex_data = json.load(f)

    out: dict = {
        "now": now.isoformat(),
        "today": today_block(now),
    }

    if args.birth:
        birth = datetime.fromisoformat(args.birth)
        if args.time_unknown:
            birth = birth.replace(hour=12, minute=0)
        personal = saju(birth, args.lon, args.sect, args.gender, args.time_unknown)
        out["personal"] = personal

        # Personal salt for I-Ching: derived from user's year+month+day pillars
        # so two people get different hexagrams at the same moment
        yp, mp, dp = personal["pillars"]["year"]["gz"], personal["pillars"]["month"]["gz"], personal["pillars"]["day"]["gz"]
        salt = sum(ZHI_LIST.index(g[1]) + 1 for g in (yp, mp, dp))
        iching = iching_meihua(now, hex_data, salt=salt)

        # Today × user analysis
        user_day_gan = personal["pillars"]["day"]["gz"][0]
        user_day_zhi = personal["pillars"]["day"]["gz"][1]
        today_gan = out["today"]["day_gan"]
        today_zhi = out["today"]["day_zhi"]
        ss = shishen_of(today_gan, user_day_gan)
        br = branch_relation(today_zhi, user_day_zhi)

        out["interaction"] = {
            "user_day_pillar":   personal["pillars"]["day"]["gz"],
            "today_day_pillar":  out["today"]["day_pillar"],
            "shishen_today_to_user_day_master": ss,
            "shishen_meta": SHISHEN_META[ss],
            "branch_relation": br,
            "branch_meta": BRANCH_META[br],
            "_for_claude": (
                "INTERPRET THIS AS TODAY'S FORTUNE ONLY — not a life reading. "
                "Use the shishen_meta + branch_meta to assign 5-category stars "
                "(overall/love/money/career/health, 2-5 each, varied distribution) "
                "and write the daily reading. Apply your 명리 knowledge but stay "
                "anchored to TODAY × THIS USER, not the user's whole life."
            ),
        }

        user_el = personal["day_master_element"]
        out["lucky"] = {
            "number": (iching["_total"] * iching["num"] + ZHI_LIST.index(user_day_zhi) * 7) % 100,
            "color": ELEMENT_COLOR[user_el],
            "direction": ELEMENT_DIRECTION[user_el],
            "based_on": f"{user_day_gan} day master ({user_el})",
        }
    else:
        iching = iching_meihua(now, hex_data, salt=0)
        today_el = out["today"]["day_element"]
        out["interaction"] = {
            "_for_claude": (
                "No birth info — write a generic daily reading from today's "
                "day pillar element + the I-Ching hexagram. Stay focused on "
                "TODAY ONLY. Suggest the user provide birth info for a real "
                "personalized reading."
            ),
        }
        out["lucky"] = {
            "number": (iching["_total"] * iching["num"]) % 100,
            "color": ELEMENT_COLOR[today_el],
            "direction": ELEMENT_DIRECTION[today_el],
            "based_on": f"today's day pillar ({today_el}) — generic",
        }

    iching.pop("_total", None)
    out["iching"] = iching

    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
