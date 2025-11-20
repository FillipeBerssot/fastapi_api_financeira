"""
Script simples para criar as tabelas no banco Postgres
usando os models SQLAchemy do projeto.

Esse script deve ser executado MANUALMENTE em desenvolvimento,
até termos migrations com Alembic.
"""

from app.core.database import engine

# IMPORTANTE: importar os models para que eles registrem as tabelas no Base.metadata
from app.models import user  # noqa: F401  # só para garantir que User é registrado
from app.models.base import Base  # ajuste o caminho se o Base estiver em outro lugar


def init_db() -> None:
    """
    Cria todas as tabelas definidas em Base.metadata no banco apontado por `engine`.
    """
    print("📦 Criando tabelas no banco de dados...")
    Base.metadata.create_all(bind=engine)
    print("✅ Tabelas criadas com sucesso!")


if __name__ == "__main__":
    init_db()
