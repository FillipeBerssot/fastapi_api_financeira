from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import get_password_hash
from app.models.user import User
from app.schemas.user import UserCreate


def get_user_by_email(db: Session, email: str) -> User | None:
    """
    Busca um usuário pelo e-mail. Retorna None se não encontrar.
    """
    stmt = select(User).where(User.email == email)
    result = db.execute(stmt).scalar_one_or_none()
    return result


def create_user(db: Session, user_in: UserCreate) -> User:
    """
    Cria um novo usuário no banco de dados, com a senha hasheada.
    """
    hashed_password = get_password_hash(user_in.password)

    db_user = User(
        email=user_in.email,
        full_name=user_in.full_name,
        hashed_password=hashed_password,
        is_active=True,
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user
