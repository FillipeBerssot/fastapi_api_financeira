from collections.abc import Generator

import pytest
from app.core.database import get_db
from app.main import app
from app.models.base import Base
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

TEST_DATABASE_URL = "sqlite:///./test_db.sqlite3"


engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    future=True,
)

TestingSessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    class_=Session,
)


def override_get_db() -> Generator[Session, None, None]:
    """
    Versão de get_db usada SOMENTE nos testes.

    Em vez de usar o Postgres (DATABASE_URL real),
    usamos a engine de testes (SQLite).
    """
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="session", autouse=True)
def create_test_database() -> Generator[None, None, None]:
    """
    Cria todas as tabelas no banco de testes antes da sessão de testes
    e apaga tudo no final (se necessário).
    """
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    yield


@pytest.fixture()
def db_session() -> Generator[Session, None, None]:
    """
    Entrega uma sessão de banco de dados para os testes que precisarem
    interagir diretamente com a base.
    """
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client() -> TestClient:
    """
    Cliente HTTP de testes para chamar os endpoints da API.
    """
    return TestClient(app)
