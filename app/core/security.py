from datetime import datetime, timedelta, timezone
from typing import Any, Final

from jose import jwt
from passlib.context import CryptContext

# Configurações de segurança
SECRET_KEY: Final[str] = "sua_chave_secreta_muito_secreta"
ALGORITHM: Final[str] = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES: Final[int] = 30


pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")


# Funções para manipular senhas
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Compara uma senha em texto puro com o hash guardado no banco.

    Retorna True se a senha corresponder ao hash, False caso contrário.
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Recebe uma senha em texto puro e devolve o hash usando bcrypt.

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
