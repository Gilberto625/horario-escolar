from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from app.config import TIMEZONE

VALID_DAYS = {"lunes", "martes", "miercoles", "miércoles", "jueves", "viernes"}

DAY_ALIASES = {
    "lunes": "lunes",
    "martes": "martes",
    "miercoles": "miercoles",
    "miércoles": "miercoles",
    "jueves": "jueves",
    "viernes": "viernes",
}

WEEKDAY_TO_SPANISH = {
    0: "lunes",
    1: "martes",
    2: "miercoles",
    3: "jueves",
    4: "viernes",
    5: "sabado",
    6: "domingo",
}


def now_mexico() -> datetime:
    return datetime.now(ZoneInfo(TIMEZONE))


def normalize_day(day: str) -> str:
    normalized = day.strip().lower()
    return DAY_ALIASES.get(normalized, normalized)


def is_valid_weekday(day: str) -> bool:
    return normalize_day(day) in {"lunes", "martes", "miercoles", "jueves", "viernes"}


def get_today_day_name() -> str:
    weekday = now_mexico().weekday()
    return WEEKDAY_TO_SPANISH[weekday]


def get_tomorrow_day_name() -> str:
    weekday = (now_mexico() + timedelta(days=1)).weekday()
    return WEEKDAY_TO_SPANISH[weekday]
