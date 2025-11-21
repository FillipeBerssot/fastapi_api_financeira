from datetime import datetime, timedelta, timezone
from typing import Any, Final

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.user import User

# Configurações de segurança
SECRET_KEY: Final[str] = "sua_chave_secreta_muito_secreta"
ALGORITHM: Final[str] = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES: Final[int] = 30


pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


# Funções para manipular senhas
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Compara uma senha em texto puro com o hash guardado no banco.

    Retorna True se a senha corresponder ao hash, False caso contrário.
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Recebe uma senha em texto puro e devolve o hash usando pbkdf2_sha256.

    É esse hash que vamos guardar no banco (campo hashed_password do User).
    """
    return pwd_context.hash(password)


# Funções para gerar o JWT
def create_access_token(
    data: dict[str, Any],
    expires_delta: timedelta | None = None,
) -> str:
    """
    Gera um token de acesso (JWT).

    - 'data': dicionário com os dados que queremos colocar no token.
        Exemplo: {"sub": email_do_usuario}
    - 'expires_delta': opcional. Se não for informado, usa o tempo padrão.
        definido em ACCESS_TOKEN_EXPIRE_MINUTES.
    """
    to_encode = data.copy()

    if expires_delta is not None:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode["exp"] = expire

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    """
    Lê o JWT do header Authorization Bearer,
    valida e retorna o usuário correspondente.
    """
    from app.services.user_service import get_user_by_email

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str | None = payload.get("sub")

        if email is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    user = get_user_by_email(db, email=email)

    if user is None:
        raise credentials_exception

    return user
