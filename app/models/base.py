from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """
    Classe Base para todos os modelos do SQLAlchemy.
    Todos os models de tabela (User, Account, Category, etc.)
    vão herdar desta classe.
    """

    pass
