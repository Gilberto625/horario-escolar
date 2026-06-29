from datetime import date, time

from app.models import ScheduleEntry, Task


def format_time(value: time) -> str:
    return value.strftime("%H:%M")


def format_date(value: date | None) -> str | None:
    return value.isoformat() if value else None


def schedule_entry_to_dict(entry: ScheduleEntry) -> dict:
    return {
        "id": entry.id,
        "subject": entry.subject,
        "startTime": format_time(entry.start_time),
        "endTime": format_time(entry.end_time),
        "professor": entry.professor,
        "classroom": entry.classroom,
        "isAdvisory": entry.is_advisory,
    }


def task_to_dict(task: Task) -> dict:
    return {
        "id": task.id,
        "subject": task.subject,
        "title": task.title,
        "description": task.description,
        "dueDate": format_date(task.due_date),
        "dueTime": format_time(task.due_time) if task.due_time else None,
        "status": task.status,
    }
