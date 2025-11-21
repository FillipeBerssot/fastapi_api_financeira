import os
from typing import Final

from dotenv import load_dotenv

load_dotenv()

DATABASE_URL: Final[str] = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError(
        "DATABASE_URL não está definida. Crie um .env ou configure"
        "a variável de ambiente."
    )
