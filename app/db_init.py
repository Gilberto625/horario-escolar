from sqlalchemy import inspect

from app.database import Base, engine
from app.models import ScheduleEntry, Task

SCHEDULE_COLUMNS = {
    "id",
    "day",
    "subject",
    "start_time",
    "end_time",
    "professor",
    "classroom",
    "is_advisory",
}

TASK_COLUMNS = {
    "id",
    "alexa_user_id",
    "subject",
    "title",
    "description",
    "due_date",
    "due_time",
    "status",
    "created_at",
    "completed_at",
}


def _table_columns(inspector, table_name: str) -> set[str]:
    if table_name not in inspector.get_table_names():
        return set()

    return {column["name"] for column in inspector.get_columns(table_name)}


def _schema_is_valid(inspector) -> bool:
    schedule_columns = _table_columns(inspector, ScheduleEntry.__tablename__)
    task_columns = _table_columns(inspector, Task.__tablename__)

    if schedule_columns and not SCHEDULE_COLUMNS.issubset(schedule_columns):
        return False

    if task_columns and not TASK_COLUMNS.issubset(task_columns):
        return False

    return True


def ensure_schema() -> None:
    if engine is None:
        raise RuntimeError("DATABASE_URL no está configurada")

    inspector = inspect(engine)

    if not _schema_is_valid(inspector):
        Base.metadata.drop_all(bind=engine)

    Base.metadata.create_all(bind=engine)
