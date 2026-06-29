from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import CORS_ORIGINS
from app.database import Base, SessionLocal, engine
from app.routers import health, schedule, tasks
from app.seeds.seed_schedule import seed_schedule


@asynccontextmanager
async def lifespan(_: FastAPI):
    if engine is None:
        raise RuntimeError("DATABASE_URL no está configurada")

    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        seed_schedule(db)
    finally:
        db.close()

    yield


app = FastAPI(
    title="Backend Horario Escolar",
    description="API para la Alexa Skill Mi Horario Escolar",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(HTTPException)
async def http_exception_handler(_: Request, exc: HTTPException):
    if isinstance(exc.detail, dict):
        return JSONResponse(status_code=exc.status_code, content=exc.detail)

    return JSONResponse(
        status_code=exc.status_code,
        content={"error": "http_error", "message": str(exc.detail)},
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(_: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "error": "validation_error",
            "message": "Los datos enviados no son válidos",
            "details": exc.errors(),
        },
    )


@app.exception_handler(Exception)
async def unhandled_exception_handler(_: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "error": "internal_error",
            "message": "Ocurrió un error inesperado en el servidor",
        },
    )


app.include_router(health.router)
app.include_router(schedule.router)
app.include_router(tasks.router)
