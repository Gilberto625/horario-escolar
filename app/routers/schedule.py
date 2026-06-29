from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import ScheduleEntry
from app.schemas import ScheduleDayResponse, ScheduleEntryResponse
from app.utils.serializers import schedule_entry_to_dict
from app.utils.timezone_utils import (
    get_today_day_name,
    get_tomorrow_day_name,
    is_valid_weekday,
    normalize_day,
)

router = APIRouter(prefix="/api/v1/schedule", tags=["schedule"])


def get_schedule_for_day(db: Session, day: str) -> ScheduleDayResponse:
    normalized_day = normalize_day(day)

    if not is_valid_weekday(normalized_day):
        raise HTTPException(
            status_code=400,
            detail={
                "error": "invalid_day",
                "message": "El día debe ser lunes, martes, miércoles, jueves o viernes",
            },
        )

    entries = (
        db.query(ScheduleEntry)
        .filter(ScheduleEntry.day == normalized_day)
        .order_by(ScheduleEntry.start_time.asc())
        .all()
    )

    return ScheduleDayResponse(
        day=normalized_day,
        entries=[ScheduleEntryResponse(**schedule_entry_to_dict(entry)) for entry in entries],
    )


@router.get("/today", response_model=ScheduleDayResponse)
def get_today_schedule(db: Session = Depends(get_db)):
    day = get_today_day_name()

    if not is_valid_weekday(day):
        return ScheduleDayResponse(day=day, entries=[])

    return get_schedule_for_day(db, day)


@router.get("/tomorrow", response_model=ScheduleDayResponse)
def get_tomorrow_schedule(db: Session = Depends(get_db)):
    day = get_tomorrow_day_name()

    if not is_valid_weekday(day):
        return ScheduleDayResponse(day=day, entries=[])

    return get_schedule_for_day(db, day)


@router.get("/day/{day}", response_model=ScheduleDayResponse)
def get_schedule_by_day(day: str, db: Session = Depends(get_db)):
    return get_schedule_for_day(db, day)
