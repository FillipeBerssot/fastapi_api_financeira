from http import HTTPStatus

from app.core.security import get_password_hash
from app.models.user import User


def test_get_current_user_success(client, db_session) -> None:
    """
    Deve retornar o usuário atual quando o token é válido.
    """

    raw_password = "senha_teste_me"

    user = User(
        email="me_user@test.com",
        full_name="Usuário Me",
        hashed_password=get_password_hash(raw_password),
        is_active=True,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    login_payload = {
        "email": user.email,
        "password": raw_password,
    }

    login_response = client.post("/auth/login", data=login_payload)
    assert login_response.status_code == HTTPStatus.OK

    token = login_response.json()["access_token"]

    me_response = client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert me_response.status_code == HTTPStatus.OK
    data = me_response.json()
    assert data["email"] == user.email
    assert data["full_name"] == user.full_name
    assert "hashed_password" not in data


def test_get_current_user_without_token(client) -> None:
    """
    Não deve permitir acessar /auth/me sem token.
    """
    response = client.get("/auth/me")

    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_get_current_user_with_invalid_token(client) -> None:
    """
    Não deve permitir acessar /auth/me com token inválido.
    """
    response = client.get(
        "/auth/me",
        headers={"Authorization": "Bearer token_invalido"},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
