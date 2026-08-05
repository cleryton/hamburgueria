"""
Teste basico para validar que a aplicacao Flask sobe corretamente.
A partir da Aula 09 (testes automatizados) este arquivo sera expandido
com testes de produtos, pedidos e estoque e etc.
"""
from src.app import create_app


def test_health_check():
    app = create_app()
    client = app.test_client()

    response = client.get("/")

    assert response.status_code == 200
    assert response.get_json()["status"] == "ok"
