from http import HTTPStatus

from fastapi import APIRouter, Depends, Form, HTTPException
from pydantic import EmailStr
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.user import UserCreate, UserRead
from app.services.user_service import create_user, get_user_by_email

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post("/register", response_model=UserRead, status_code=HTTPStatus.CREATED)
def register_user(
    email: EmailStr = Form(...),
    full_name: str = Form(...),
    password: str = Form(...),
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
    existing_user = get_user_by_email(db, email=email)

    if existing_user:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Email já está em uso.",
        )

    user_in = UserCreate(
        email=email,
        full_name=full_name,
        password=password,
    )

    new_user = create_user(db, user_in=user_in)

    return new_user
