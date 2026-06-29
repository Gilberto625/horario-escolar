from datetime import time

from sqlalchemy.orm import Session

from app.models import ScheduleEntry

SCHEDULE_SEED = [
    # Lunes (8)
    ("lunes", "Dirección de Equipos de Alto Rendimiento", "13:20", "14:10", "Lic. Beatriz Hernández Hernández", "Salón K9", True),
    ("lunes", "Inglés VIII", "14:10", "15:00", "Lic. Norma Hernández Gámez", "Salón K10", True),
    ("lunes", "Desarrollo Web Integral", "15:00", "15:50", "MTI. Juvencio Mendoza Castelán", "Lab 4", False),
    ("lunes", "Desarrollo Web Integral", "15:50", "16:40", "MTI. Juvencio Mendoza Castelán", "Lab 4", False),
    ("lunes", "Desarrollo para Dispositivos Inteligentes", "16:40", "17:30", "MCE. Ana María Felipe Redondo", "Lab 3", False),
    ("lunes", "Extracción de Conocimiento en Bases de Datos", "17:30", "18:20", "Dr. Efrén Juárez Castillo", "Lab 3", False),
    ("lunes", "Extracción de Conocimiento en Bases de Datos", "18:20", "19:10", "Dr. Efrén Juárez Castillo", "Lab 3", False),
    ("lunes", "Extracción de Conocimiento en Bases de Datos", "19:10", "20:00", "Dr. Efrén Juárez Castillo", "Lab 3", False),
    # Martes (6)
    ("martes", "Dirección de Equipos de Alto Rendimiento", "15:00", "15:50", "Lic. Beatriz Hernández Hernández", "Salón K10", False),
    ("martes", "Dirección de Equipos de Alto Rendimiento", "15:50", "16:40", "Lic. Beatriz Hernández Hernández", "Salón K10", False),
    ("martes", "Administración de Proyectos de TI", "16:40", "17:30", "Dra. Gladys Beatriz Paulín Castillo", "Salón K10", False),
    ("martes", "Administración de Proyectos de TI", "17:30", "18:20", "Dra. Gladys Beatriz Paulín Castillo", "Salón K10", False),
    ("martes", "Desarrollo para Dispositivos Inteligentes", "18:20", "19:10", "MCE. Ana María Felipe Redondo", "Lab 3", False),
    ("martes", "Desarrollo para Dispositivos Inteligentes", "19:10", "20:00", "MCE. Ana María Felipe Redondo", "Lab 3", False),
    # Miércoles (8)
    ("miercoles", "Administración de Proyectos de TI", "13:20", "14:10", "Dra. Gladys Beatriz Paulín Castillo", "Salón K8", True),
    ("miercoles", "Extracción de Conocimiento en Bases de Datos", "14:10", "15:00", "Dr. Efrén Juárez Castillo", "Lab 3", True),
    ("miercoles", "Inglés VIII", "15:00", "15:50", "Lic. Norma Hernández Gámez", "Salón K10", False),
    ("miercoles", "Inglés VIII", "15:50", "16:40", "Lic. Norma Hernández Gámez", "Salón K10", False),
    ("miercoles", "Desarrollo para Dispositivos Inteligentes", "16:40", "17:30", "MCE. Ana María Felipe Redondo", "Lab 3", False),
    ("miercoles", "Desarrollo para Dispositivos Inteligentes", "17:30", "18:20", "MCE. Ana María Felipe Redondo", "Lab 3", False),
    ("miercoles", "Desarrollo Web Integral", "18:20", "19:10", "MTI. Juvencio Mendoza Castelán", "Lab 4", False),
    ("miercoles", "Desarrollo Web Integral", "19:10", "20:00", "MTI. Juvencio Mendoza Castelán", "Lab 4", False),
    # Jueves (5)
    ("jueves", "Desarrollo para Dispositivos Inteligentes", "14:10", "15:00", "MCE. Ana María Felipe Redondo", "Lab 3", True),
    ("jueves", "Administración de Proyectos de TI", "15:00", "15:50", "Dra. Gladys Beatriz Paulín Castillo", "Salón K10", False),
    ("jueves", "Extracción de Conocimiento en Bases de Datos", "15:50", "16:40", "Dr. Efrén Juárez Castillo", "Lab 3", False),
    ("jueves", "Extracción de Conocimiento en Bases de Datos", "16:40", "17:30", "Dr. Efrén Juárez Castillo", "Lab 3", False),
    ("jueves", "Tutorías", "17:30", "18:20", "Dra. Gladys Beatriz Paulín Castillo", "Salón K10", False),
    # Viernes (5)
    ("viernes", "Desarrollo Web Integral", "14:10", "15:00", "MTI. Juvencio Mendoza Castelán", "Lab 4", True),
    ("viernes", "Desarrollo Web Integral", "15:00", "15:50", "MTI. Juvencio Mendoza Castelán", "Lab 4", False),
    ("viernes", "Desarrollo Web Integral", "15:50", "16:40", "MTI. Juvencio Mendoza Castelán", "Lab 4", False),
    ("viernes", "Inglés VIII", "16:40", "17:30", "Lic. Norma Hernández Gámez", "Salón K10", False),
    ("viernes", "Inglés VIII", "17:30", "18:20", "Lic. Norma Hernández Gámez", "Salón K10", False),
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
