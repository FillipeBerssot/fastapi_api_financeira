def test_health_endpoint(client) -> None:
    """
    Verifica se o endpoint /health está retornando status 200 e o JSON esperado.
    """
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "OK"}
