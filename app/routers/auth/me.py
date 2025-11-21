from fastapi import APIRouter, Depends

from app.core.security import get_current_user
from app.models.user import User
from app.schemas.user import UserRead

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.get("/me", response_model=UserRead)
def read_current_user(
    current_user: User = Depends(get_current_user),
) -> UserRead:
    """
    Retorna os dados do usuário atualmente autenticado.
    """
    return current_user
