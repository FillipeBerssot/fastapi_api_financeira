from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.user import UserCreate, UserRead
from app.services.user_service import create_user, get_user_by_email

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post(
    "/register",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
)
def register_user(
    user_in: UserCreate,
    db: Session = Depends(get_db),
) -> UserRead:
    """
    Registra um novo usuário no sistema.

    Fluxo:
    - Recebe email, full_name e password (UserCreate).
    - Verifica se já existe usuário com o mesmo email.
    - Se existir, retorna 400.
    - Se não existir, cria o usuário e retorna os dados (UserRead).
    """
    existing_user = get_user_by_email(db, user_in.email)
    if existing_user is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email já está em uso.",
        )

    new_user = create_user(db, user_in)

    return new_user
