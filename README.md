# Backend Horario Escolar

API REST para la Alexa Skill **Mi Horario Escolar**. Expone horario escolar y tareas pendientes consumiendo PostgreSQL (Neon).

## Stack

- FastAPI
- SQLAlchemy
- PostgreSQL (Neon)
- Zona horaria `America/Mexico_City`

## Estructura

```
backend-horario-escolar/
├── app/
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── routers/
│   │   ├── health.py
│   │   ├── schedule.py
│   │   └── tasks.py
│   ├── seeds/
│   │   └── seed_schedule.py
│   └── utils/
├── requirements.txt
├── render.yaml
└── .env.example
```

## Configurar DATABASE_URL

1. Crea un proyecto en [Neon](https://neon.tech).
2. Crea una base de datos PostgreSQL.
3. Copia la connection string (Connection string → PostgreSQL).
4. Debe incluir SSL:

```
postgresql://usuario:password@ep-xxxx.region.aws.neon.tech/neondb?sslmode=require
```

5. Crea tu archivo local:

```powershell
copy .env.example .env
```

6. Pega la URL en `DATABASE_URL` dentro de `.env`.

## Ejecución local

```powershell
cd backend-horario-escolar
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
# Edita .env y configura DATABASE_URL
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Al iniciar, el backend:

- crea las tablas si no existen
- ejecuta el seed del horario escolar si la tabla está vacía

Documentación interactiva: [http://localhost:8000/docs](http://localhost:8000/docs)

## Probar endpoints

### Health

```powershell
curl http://localhost:8000/health
```

### Horario de hoy

```powershell
curl http://localhost:8000/api/v1/schedule/today
```

### Horario de mañana

```powershell
curl http://localhost:8000/api/v1/schedule/tomorrow
```

### Horario por día

```powershell
curl http://localhost:8000/api/v1/schedule/day/lunes
```

### Tareas pendientes

```powershell
curl "http://localhost:8000/api/v1/tasks/pending?alexaUserId=test-user-123"
```

### Crear tarea

```powershell
curl -X POST http://localhost:8000/api/v1/tasks ^
  -H "Content-Type: application/json" ^
  -d "{\"alexaUserId\":\"test-user-123\",\"subject\":\"Desarrollo Web Integral\",\"title\":\"Entregar proyecto\",\"description\":\"Entregar proyecto\",\"dueDate\":\"2026-07-03\",\"dueTime\":\"18:00\"}"
```

### Completar tarea por ID

```powershell
curl -X PATCH http://localhost:8000/api/v1/tasks/1/complete ^
  -H "Content-Type: application/json" ^
  -d "{\"alexaUserId\":\"test-user-123\"}"
```

### Completar tarea por criterio (opcional)

```powershell
curl -X POST http://localhost:8000/api/v1/tasks/complete-by-criteria ^
  -H "Content-Type: application/json" ^
  -d "{\"alexaUserId\":\"test-user-123\",\"subject\":\"Desarrollo Web Integral\"}"
```

## Deploy en Render

1. Sube este proyecto a GitHub.
2. En [Render](https://render.com), crea un **Web Service**.
3. Conecta el repositorio.
4. Render detectará `render.yaml` o configura manualmente:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Agrega variable de entorno:
   - `DATABASE_URL` = connection string de Neon
   - `TIMEZONE` = `America/Mexico_City`
6. Despliega y copia la URL pública, por ejemplo:
   - `https://backend-horario-escolar.onrender.com`
7. En la Lambda de Alexa configura:
   - `BACKEND_API_URL=https://backend-horario-escolar.onrender.com`

## Endpoints

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/health` | Health check |
| GET | `/api/v1/schedule/today` | Horario de hoy (CDMX) |
| GET | `/api/v1/schedule/tomorrow` | Horario de mañana (CDMX) |
| GET | `/api/v1/schedule/day/{day}` | Horario por día |
| GET | `/api/v1/tasks/pending` | Tareas pendientes |
| POST | `/api/v1/tasks` | Crear tarea |
| PATCH | `/api/v1/tasks/{id}/complete` | Completar tarea |
| POST | `/api/v1/tasks/complete-by-criteria` | Completar por materia/descripción |

## Compatibilidad con Alexa Skill

La skill espera:

- horario en campo `entries` (también soportado como `classes` en la skill)
- tareas en campo `tasks`
- creación con `time` o `dueTime`
- `alexaUserId` en query/body para filtrar tareas por usuario

## Notas

- El horario se guarda en PostgreSQL; los endpoints no tienen horario hardcodeado.
- Si hoy o mañana caen en sábado o domingo, la API responde con `entries: []`.
- El seed solo corre cuando `schedule_entries` está vacía.
