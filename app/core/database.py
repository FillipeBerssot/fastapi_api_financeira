from collections.abc import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from app.core.config import DATABASE_URL
from app.models.base import Base


engine = create_engine(
    DATABASE_URL,
    echo=True,
    future=True,
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    class_=Session,
)

def get_db() -> Generator[Session, None, None]:
    """"
    Dependência para ser usada nas rotas do FastAPI.
    
    Ela cria uma sessão com o banco (SessionLocal),
    entrega essa sessão para a rota (via yield),
    e garante que a sessão será fechada no final.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()