import os
import re

from dotenv import load_dotenv

load_dotenv()


def sanitize_database_url(raw_url: str) -> str:
    if not raw_url:
        return ""

    url = raw_url.strip()
    url = re.sub(r"^psql\s+", "", url, flags=re.IGNORECASE).strip()

    while url and url[0] in "'\"":
        url = url[1:].strip()
    while url and url[-1] in "'\"":
        url = url[:-1].strip()

    match = re.search(r"(postgres(?:ql)?://\S+)", url, re.IGNORECASE)
    if match:
        url = match.group(1).rstrip("'\"),;")

    if url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql://", 1)

    return url


DATABASE_URL = sanitize_database_url(os.getenv("DATABASE_URL", ""))
TIMEZONE = os.getenv("TIMEZONE", "America/Mexico_City")
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",")
