from fastapi.testclient import TestClient
from main import app


client = TestClient(app)

def test_listar_produtos_sem_token():
    """Deve negar acesso se não houver token"""
    response = client.get("/produtos")
    assert response.status_code == 401

def test_login_sucesso():
    """Deve retornar um token para credenciais válidas"""
    response = client.post(
        "/token",
        data={"username": "admin", "password": "thigasapi111"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_criar_produto_com_preco_invalido():
    """Deve validar o Field(gt=0) do Pydantic"""
    # Primeiro obtemos o token...
    login_res = client.post("/token", data={"username": "admin", "password": "thigasapi111"})
    token = login_res.json()["access_token"]
    
    # Tentamos criar com preço zero
    response = client.post(
        "/produtos",
        json={"nome": "Teclado", "preco": 0, "descricao": "Invalido"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 422