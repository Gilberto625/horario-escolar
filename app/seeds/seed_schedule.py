from datetime import time

from sqlalchemy.orm import Session

from app.models import ScheduleEntry

SCHEDULE_SEED = [
    # Lunes
    ("lunes", "Desarrollo Web Integral", "15:00", "15:50", "MTI. Juvencio Mendoza Castelán", "Lab 4", False),
    ("lunes", "Desarrollo Web Integral", "16:00", "16:50", "MTI. Juvencio Mendoza Castelán", "Lab 4", False),
    ("lunes", "Extracción de Conocimiento en Bases de Datos", "17:00", "17:50", "M.I. Ana Lilia Ramírez", "Aula 12", False),
    ("lunes", "Extracción de Conocimiento en Bases de Datos", "18:00", "18:50", "M.I. Ana Lilia Ramírez", "Aula 12", False),
    # Martes
    ("martes", "Desarrollo para Dispositivos Inteligentes", "15:00", "15:50", "M.I. Carlos Eduardo Ruiz", "Lab 2", False),
    ("martes", "Desarrollo para Dispositivos Inteligentes", "16:00", "16:50", "M.I. Carlos Eduardo Ruiz", "Lab 2", False),
    ("martes", "Inglés VIII", "17:00", "17:50", "Lic. Patricia Morales", "Aula 8", False),
    ("martes", "Inglés VIII", "18:00", "18:50", "Lic. Patricia Morales", "Aula 8", False),
    # Miércoles
    ("miercoles", "Administración de Proyectos de TI", "15:00", "15:50", "M.I. Roberto Sánchez", "Aula 5", False),
    ("miercoles", "Administración de Proyectos de TI", "16:00", "16:50", "M.I. Roberto Sánchez", "Aula 5", False),
    ("miercoles", "Dirección de Equipos de Alto Rendimiento", "17:00", "17:50", "M.I. Laura Hernández", "Aula 3", False),
    ("miercoles", "Dirección de Equipos de Alto Rendimiento", "18:00", "18:50", "M.I. Laura Hernández", "Aula 3", False),
    # Jueves
    ("jueves", "Desarrollo Web Integral", "15:00", "15:50", "MTI. Juvencio Mendoza Castelán", "Lab 4", False),
    ("jueves", "Desarrollo Web Integral", "16:00", "16:50", "MTI. Juvencio Mendoza Castelán", "Lab 4", True),
    ("jueves", "Extracción de Conocimiento en Bases de Datos", "17:00", "17:50", "M.I. Ana Lilia Ramírez", "Lab 1", False),
    ("jueves", "Extracción de Conocimiento en Bases de Datos", "18:00", "18:50", "M.I. Ana Lilia Ramírez", "Lab 1", False),
    # Viernes
    ("viernes", "Desarrollo para Dispositivos Inteligentes", "15:00", "15:50", "M.I. Carlos Eduardo Ruiz", "Lab 2", False),
    ("viernes", "Desarrollo para Dispositivos Inteligentes", "16:00", "16:50", "M.I. Carlos Eduardo Ruiz", "Lab 2", True),
    ("viernes", "Tutorías", "17:00", "17:50", "Docente tutor", "Cubículo 9C", True),
]


def parse_time(value: str) -> time:
    hour, minute = value.split(":")
    return time(int(hour), int(minute))


def seed_schedule(db: Session) -> None:
    existing = db.query(ScheduleEntry).count()
    if existing > 0:
        return

    for day, subject, start, end, professor, classroom, is_advisory in SCHEDULE_SEED:
        db.add(
            ScheduleEntry(
                day=day,
                subject=subject,
                start_time=parse_time(start),
                end_time=parse_time(end),
                professor=professor,
                classroom=classroom,
                is_advisory=is_advisory,
            )
        )

    db.commit()
