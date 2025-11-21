from http import HTTPStatus

from app.models.user import User


def test_register_user_success(client, db_session) -> None:
    """
    Deve registrar um novo usuário com sucesso e salvar no banco.
    """
    payload = {
        "email": "novo_usuario@test.com",
        "full_name": "Novo Usuário",
        "password": "senha_secreta",
    }

    response = client.post("/auth/register", data=payload)

    assert response.status_code == HTTPStatus.CREATED

    data = response.json()
    assert data["email"] == payload["email"]
    assert data["full_name"] == payload["full_name"]
    assert "hashed_password" not in data
    assert "password" not in data

    user_in_db = db_session.query(User).filter_by(email=payload["email"]).first()

    assert user_in_db is not None
    assert user_in_db.full_name == payload["full_name"]


def test_register_user_with_existing_email(client, db_session) -> None:
    """
    Não deve permitir registrar dois usuários com o mesmo e-mail.
    """
    existing_user = User(
        email="ja_existe@test.com",
        full_name="Usuário Existente",
        hashed_password="hash_qualquer",
        is_active=True,
    )
    db_session.add(existing_user)
    db_session.commit()

    payload = {
        "email": "ja_existe@test.com",
        "full_name": "Outro Usuário",
        "password": "outra_senha",
    }

    response = client.post("/auth/register", data=payload)

    assert response.status_code == HTTPStatus.BAD_REQUEST

    data = response.json()
    assert data["detail"] == "Email já está em uso."
