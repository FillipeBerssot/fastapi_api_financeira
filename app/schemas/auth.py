from typing import Any

from pydantic import BaseModel


class Token(BaseModel):
    """
    Representa o token de acesso retornado após o login.
    """

    access_token: str
    token_type: str


class TokenData(BaseModel):
    """
    Dados mínimos extraídos de um token JWT válido.

    - 'sub' geralmente representa o "subject" do token,
        por exemplo, o e-mail ou id do usuário.
    - 'extra' pode guardar informações adicionais, se quisermos.
    """

    sub: str | None = None
    extra: dict[str, Any] | None = None
