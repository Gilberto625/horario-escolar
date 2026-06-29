from datetime import date, time

from pydantic import BaseModel, ConfigDict, Field


class HealthResponse(BaseModel):
    status: str
    service: str


class ScheduleEntryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    subject: str
    startTime: str
    endTime: str
    professor: str
    classroom: str
    isAdvisory: bool


class ScheduleDayResponse(BaseModel):
    day: str
    entries: list[ScheduleEntryResponse]


class TaskResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    subject: str
    title: str
    description: str | None = None
    dueDate: str | None = None
    dueTime: str | None = None
    status: str


class TaskListResponse(BaseModel):
    tasks: list[TaskResponse]


class TaskCreateRequest(BaseModel):
    alexaUserId: str | None = None
    subject: str
    title: str
    description: str | None = None
    dueDate: str | None = None
    dueTime: str | None = None
    time: str | None = Field(default=None, description="Alias compatible con Alexa Skill")


class TaskCompleteRequest(BaseModel):
    alexaUserId: str | None = None


class TaskCompleteByCriteriaRequest(BaseModel):
    alexaUserId: str | None = None
    subject: str | None = None
    taskDescription: str | None = None


class TaskCreatedResponse(BaseModel):
    task: TaskResponse


class ErrorResponse(BaseModel):
    error: str
    message: str
