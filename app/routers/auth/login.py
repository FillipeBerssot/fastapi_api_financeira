from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import create_access_token, verify_password
from app.schemas.auth import Token
from app.services.user_service import get_user_by_email

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
) -> Token:
    """
    Endpoint de login.

    Fluxo:
    - Busca o usuário pelo e-mail.
    - Se não existir, retorna erro 401.
    - Se existir, verifica a senha.
    - Se a senha estiver correta, gera e retorna um token JWT.
    """
    email = form_data.username
    password = form_data.password

    user = get_user_by_email(db, email=email)

    if (user is None) or (not verify_password(password, user.hashed_password)):
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Email ou senha inválidos.",
        )

    access_token = create_access_token({"sub": user.email})

    return Token(
        access_token=access_token,
        token_type="bearer",
    )
