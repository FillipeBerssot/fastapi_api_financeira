from datetime import datetime

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    """
    Campos comuns entre vários usos do usuário (criação, leitura, etc).
    """

    email: EmailStr
    full_name: str | None = None


class UserCreate(UserBase):
    """
    Schema usado quando um novo usuário será criado (input).
    """

    password: str


class UserRead(UserBase):
    """
    Schema usado para devolver informações do usuário (output).
    """

    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        # Permite criar este schema a partir de um objeto ORM (User do SQLAlchemy)
        from_attributes = True
