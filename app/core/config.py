from typing import Final
import os


DATABASE_URL: Final[str] = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://user:password@localhost:5432/finance_db",
)