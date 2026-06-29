import os

from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "")
TIMEZONE = os.getenv("TIMEZONE", "America/Mexico_City")
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",")
