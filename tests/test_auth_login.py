from http import HTTPStatus

from app.core.security import get_password_hash
from app.models.user import User


def test_login_success(client, db_session) -> None:
    """
    Deve permitir login com credenciais corretas e retornar um token de acesso.
    """
    raw_password = "senha_super_secreta"

    user = User(
        email="login_success@test.com",
        full_name="Usuário Login Sucesso",
        hashed_password=get_password_hash(raw_password),
        is_active=True,
    )
    db_session.add(user)
    db_session.commit()

    payload = {
        "username": "login_success@test.com",
        "password": raw_password,
    }

    response = client.post("/auth/login", data=payload)

    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert isinstance(data["access_token"], str)
    assert len(data["access_token"]) > 0


def test_login_invalid_password(client, db_session) -> None:
    """
    Não deve permitir login com senha incorreta.
    """
    correct_password = "senha_correta"

    user = User(
        email="login_erro_senha@test.com",
        full_name="Usuário Senha Errada",
        hashed_password=get_password_hash(correct_password),
        is_active=True,
    )
    db_session.add(user)
    db_session.commit()

    payload = {
        "username": "login_erro_senha@test.com",
        "password": "senha_errada",
    }

    response = client.post("/auth/login", data=payload)

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    data = response.json()
    assert data["detail"] == "Email ou senha inválidos."


def test_login_non_existent_user(client) -> None:
    """
    Não deve permitir login com usuário que não existe.
    """
    payload = {
        "username": "não_existe@test.com",
        "password": "qualquer_senha",
    }

    response = client.post("/auth/login", data=payload)

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    data = response.json()
    assert data["detail"] == "Email ou senha inválidos."
