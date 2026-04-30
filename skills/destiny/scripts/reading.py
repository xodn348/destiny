#!/usr/bin/env python3
"""
destiny reading — daily fortune (default) or personalized birth-chart reading.

Daily mode (no --birth):
  - Today's day pillar (Heavenly Stem + Earthly Branch) from 만세력
  - One I-Ching hexagram via 매화역수 시점법 (plum-blossom time divination)
  - Lucky number / color / direction derived from the day pillar + hexagram

Personal mode (--birth ISO):
  - Above, plus a real Four Pillars chart with all classical corrections:
      * 진태양시 (true solar time) by birthplace longitude
      * Korean DST (1987-05-10 ~ 1988-10-09)
      * 야자시(default) vs 조자시 selection
      * 24절기 boundaries for month pillar (handled by lunar-python)
  - 십신 (Ten Gods) relationships, 납음 element, 대운 (10-year cycles)
  - Interaction between today's day pillar and the user's day pillar

Outputs JSON. Claude/the skill interprets it.

Usage:
    reading.py                      # daily-only
    reading.py --birth 1992-08-15T14:30 --lon 126.9784 --gender m
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
GAN_LIST = ["甲","乙","丙","丁","戊","己","庚","辛","壬","癸"]

# 천간 → 오행 + 음양
GAN_ELEMENT = {
    "甲":("Wood","yang"),"乙":("Wood","yin"),
    "丙":("Fire","yang"),"丁":("Fire","yin"),
    "戊":("Earth","yang"),"己":("Earth","yin"),
    "庚":("Metal","yang"),"辛":("Metal","yin"),
    "壬":("Water","yang"),"癸":("Water","yin"),
}
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


def korean_dst(dt: datetime) -> bool:
    return datetime(1987, 5, 10, 2, 0) <= dt < datetime(1988, 10, 9, 3, 0)


def true_solar_offset_minutes(longitude: float) -> int:
    return round((longitude - KST_STANDARD_LON) * 4)


def gz_to_ko(gz: str) -> str:
    if len(gz) != 2:
        return gz
    return GAN_KO.get(gz[0], gz[0]) + ZHI_KO.get(gz[1], gz[1])


def derive_lucky(day_gan: str, day_zhi: str, hex_num: int, mh_total: int) -> dict:
    element, _ = GAN_ELEMENT.get(day_gan, ("Earth", "yang"))
    return {
        "number": (mh_total * hex_num) % 100,
        "color": ELEMENT_COLOR[element],
        "direction": ELEMENT_DIRECTION[element],
        "element_of_today": element,
    }


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

    shishen = {
        "year_gan":  ec.getYearShiShenGan(),
        "month_gan": ec.getMonthShiShenGan(),
        "year_zhi":  list(ec.getYearShiShenZhi()),
        "month_zhi": list(ec.getMonthShiShenZhi()),
        "day_zhi":   list(ec.getDayShiShenZhi()),
    }
    if not time_unknown:
        shishen["hour_gan"] = ec.getTimeShiShenGan()
        shishen["hour_zhi"] = list(ec.getTimeShiShenZhi())

    da_yun_list = []
    try:
        for d in ec.getYun(1 if gender == "m" else 0).getDaYun()[:8]:
            gz = d.getGanZhi()
            da_yun_list.append({
                "start_year": d.getStartYear(),
                "start_age":  d.getStartAge(),
                "ganzhi":     gz,
                "ganzhi_ko":  gz_to_ko(gz),
            })
    except Exception:
        pass

    return {
        "input": {
            "birth_clock_local": birth_clock.isoformat(),
            "longitude": longitude,
            "sect_rule": "야자시(Korean default)" if sect == 2 else "조자시",
            "dst_applied": dst,
            "true_solar_offset_minutes": offset_min,
            "corrected_for_calculation": corrected.isoformat(),
            "lunar_birth": f"{lunar.getYearInChinese()}년 {lunar.getMonthInChinese()}월 {lunar.getDayInChinese()}일",
            "gender": gender,
            "time_unknown": time_unknown,
        },
        "pillars": pillars,
        "day_master": pillars["day"]["gz"][0],
        "day_master_element": GAN_ELEMENT.get(pillars["day"]["gz"][0], ("?", "?"))[0],
        "shishen": shishen,
        "da_yun": da_yun_list,
    }


def today_block(now: datetime, user_day_gz: str | None = None):
    s = Solar.fromYmdHms(now.year, now.month, now.day, now.hour, now.minute, 0)
    l = s.getLunar()
    out = {
        "date": now.strftime("%Y-%m-%d %A"),
        "year_pillar":  l.getYearInGanZhi(),
        "month_pillar": l.getMonthInGanZhi(),
        "day_pillar":   l.getDayInGanZhi(),
        "day_gan":      l.getDayGan(),
        "day_zhi":      l.getDayZhi(),
        "day_element":  GAN_ELEMENT.get(l.getDayGan(), ("?", "?"))[0],
        "lunar_date":   f"{l.getYearInChinese()}년 {l.getMonthInChinese()}월 {l.getDayInChinese()}일",
    }
    if user_day_gz and len(user_day_gz) == 2:
        out["interaction_with_user"] = {
            "user_day_pillar":  user_day_gz,
            "today_day_pillar": l.getDayInGanZhi(),
            "note": "Look for 합/충/형/파/해 between user_day and today_day in interpretation.",
        }
    return out


def iching_meihua(now: datetime, hex_data: dict) -> dict:
    s = Solar.fromYmdHms(now.year, now.month, now.day, now.hour, now.minute, 0)
    l = s.getLunar()
    y = ZHI_LIST.index(l.getYearZhi()) + 1
    m = abs(l.getMonth())
    d = abs(l.getDay())
    h = ((now.hour + 1) // 2) % 12 + 1
    upper = (y + m + d) % 8 or 8
    total = y + m + d + h
    lower = total % 8 or 8
    moving = total % 6 or 6
    info = hex_data[f"{upper},{lower}"]
    return {
        "method": "매화역수 시점법 (plum-blossom time divination)",
        "upper_trigram": list(TRIGRAM[upper]),
        "lower_trigram": list(TRIGRAM[lower]),
        "moving_line": moving,
        "_mh_total": total,
        **info,
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--birth", help="ISO datetime of birth in local clock at birthplace, e.g. 1992-08-15T14:30")
    p.add_argument("--lon", type=float, default=SEOUL_LON,
                   help="Birthplace longitude in degrees east. Seoul=126.9784, Tokyo=139.69, NYC=-74.01")
    p.add_argument("--sect", type=int, default=2, choices=[1, 2],
                   help="Hour-pillar rule for personal mode: 1=조자시, 2=야자시(Korean default)")
    p.add_argument("--gender", choices=["m", "f"], default="m")
    p.add_argument("--time-unknown", action="store_true",
                   help="Birth time unknown — skip hour pillar (still produces 7 characters)")
    args = p.parse_args()

    now = datetime.now()
    here = Path(__file__).parent
    with open(here / "iching_64.json", encoding="utf-8") as f:
        hex_data = json.load(f)

    iching = iching_meihua(now, hex_data)
    mh_total = iching.pop("_mh_total")

    out: dict = {
        "now": now.isoformat(),
        "today": today_block(now),
        "iching": iching,
    }

    if args.birth:
        birth = datetime.fromisoformat(args.birth)
        if args.time_unknown:
            birth = birth.replace(hour=12, minute=0)
        saju_result = saju(birth, args.lon, args.sect, args.gender, args.time_unknown)
        out["personal"] = saju_result
        out["today"] = today_block(now, user_day_gz=saju_result["pillars"]["day"]["gz"])

    out["lucky"] = derive_lucky(
        out["today"]["day_gan"],
        out["today"]["day_zhi"],
        iching["num"],
        mh_total,
    )

    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
