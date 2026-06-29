from datetime import date, datetime

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Task
from app.schemas import (
    TaskCompleteByCriteriaRequest,
    TaskCompleteRequest,
    TaskCreateRequest,
    TaskCreatedResponse,
    TaskListResponse,
    TaskResponse,
)
from app.utils.serializers import task_to_dict
from app.utils.timezone_utils import now_mexico

router = APIRouter(prefix="/api/v1/tasks", tags=["tasks"])


def parse_date(value: str | None) -> date | None:
    if not value:
        return None
    try:
        return date.fromisoformat(value)
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail={"error": "invalid_date", "message": "dueDate debe tener formato YYYY-MM-DD"},
        ) from exc


def parse_time(value: str | None):
    if not value:
        return None
    try:
        hour, minute = value.split(":")
        return datetime.strptime(f"{hour}:{minute}", "%H:%M").time()
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail={"error": "invalid_time", "message": "dueTime debe tener formato HH:MM"},
        ) from exc


def get_task_or_404(db: Session, task_id: int) -> Task:
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(
            status_code=404,
            detail={"error": "task_not_found", "message": "Tarea no encontrada"},
        )
    return task


def ensure_task_belongs_to_user(task: Task, alexa_user_id: str | None) -> None:
    if not alexa_user_id:
        return

    if task.alexa_user_id and task.alexa_user_id != alexa_user_id:
        raise HTTPException(
            status_code=403,
            detail={"error": "forbidden", "message": "La tarea no pertenece a este usuario"},
        )


@router.get("/pending", response_model=TaskListResponse)
def get_pending_tasks(
    alexaUserId: str | None = Query(default=None),
    db: Session = Depends(get_db),
):
    query = db.query(Task).filter(Task.status == "pending")

    if alexaUserId:
        query = query.filter(Task.alexa_user_id == alexaUserId)

    tasks = query.order_by(Task.due_date.asc().nullslast(), Task.due_time.asc().nullslast()).all()
    return TaskListResponse(tasks=[TaskResponse(**task_to_dict(task)) for task in tasks])


@router.post("", response_model=TaskCreatedResponse, status_code=201)
def create_task(payload: TaskCreateRequest, db: Session = Depends(get_db)):
    due_time_value = payload.dueTime or payload.time

    task = Task(
        alexa_user_id=payload.alexaUserId,
        subject=payload.subject,
        title=payload.title,
        description=payload.description or payload.title,
        due_date=parse_date(payload.dueDate),
        due_time=parse_time(due_time_value),
        status="pending",
    )

    db.add(task)
    db.commit()
    db.refresh(task)

    return TaskCreatedResponse(task=TaskResponse(**task_to_dict(task)))


@router.patch("/{task_id}/complete", response_model=TaskCreatedResponse)
def complete_task(
    task_id: int,
    payload: TaskCompleteRequest,
    db: Session = Depends(get_db),
):
    task = get_task_or_404(db, task_id)
    ensure_task_belongs_to_user(task, payload.alexaUserId)

    if task.status == "completed":
        return TaskCreatedResponse(task=TaskResponse(**task_to_dict(task)))

    task.status = "completed"
    task.completed_at = now_mexico()
    db.commit()
    db.refresh(task)

    return TaskCreatedResponse(task=TaskResponse(**task_to_dict(task)))


@router.post("/complete-by-criteria", response_model=TaskCreatedResponse)
def complete_task_by_criteria(payload: TaskCompleteByCriteriaRequest, db: Session = Depends(get_db)):
    if not payload.subject and not payload.taskDescription:
        raise HTTPException(
            status_code=400,
            detail={
                "error": "missing_criteria",
                "message": "Debes enviar subject o taskDescription",
            },
        )

    query = db.query(Task).filter(Task.status == "pending")

    if payload.alexaUserId:
        query = query.filter(Task.alexa_user_id == payload.alexaUserId)

    tasks = query.all()
    matches = []

    for task in tasks:
        if payload.subject and task.subject.lower() == payload.subject.lower():
            matches.append(task)
            continue
        if payload.taskDescription and payload.taskDescription.lower() in task.title.lower():
            matches.append(task)

    if len(matches) == 0:
        raise HTTPException(
            status_code=404,
            detail={"error": "task_not_found", "message": "No se encontró una tarea que coincida"},
        )

    if len(matches) > 1:
        raise HTTPException(
            status_code=409,
            detail={
                "error": "multiple_matches",
                "message": "Hay varias tareas que coinciden. Usa el ID o toca la tarea en pantalla.",
            },
        )

    task = matches[0]
    task.status = "completed"
    task.completed_at = now_mexico()
    db.commit()
    db.refresh(task)

    return TaskCreatedResponse(task=TaskResponse(**task_to_dict(task)))
