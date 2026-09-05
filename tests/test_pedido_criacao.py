from fastapi.testclient import TestClient

from main import app
from models import Produto, Categoria

client = TestClient(app)


def test_criar_pedido_com_carrinho_vazio(db):
    
    client.post(
        "/usuarios",
        json={
            "name": "Pedro",
            "email": "pedro@teste.com",
            "password": "Pedro123@"
        }
    )

    login = client.post(
        "/usuarios/login",
        json={
            "email": "pedro@teste.com",
            "password": "Pedro123@"
        }
    )

    token = login.json()["access_token"]

    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = client.post(
        "/pedidos",
        headers=headers
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Carrinho vazio."


def test_criar_pedido_com_estoque_insuficiente(db):

    client.post(
        "/usuarios",
        json={
            "name": "Pedro",
            "email": "pedro@teste.com",
            "password": "Pedro123@"
        }
    )

    login = client.post(
        "/usuarios/login",
        json={
            "email": "pedro@teste.com",
            "password": "Pedro123@"
        }
    )

    token = login.json()["access_token"]

    headers = {
        "Authorization": f"Bearer {token}"
    }

    categoria = Categoria(name="Geek")

    db.add(categoria)
    db.commit()
    db.refresh(categoria)

    produto = Produto(
        name="Caneca Naruto",
        price=50,
        estoque=1,
        category_id=categoria.id
    )

    db.add(produto)
    db.commit()
    db.refresh(produto)

    response = client.post(
        "/carrinho",
        json={
            "produto_id": produto.id,
            "quantidade": 1
        },
        headers=headers
    )

    assert response.status_code == 200

    produto.estoque = 0
    db.commit()

    response = client.post(
        "/pedidos",
        headers=headers
    )

    assert response.status_code == 400
    assert response.json()["detail"] == (
        "Estoque insuficiente para o produto: Caneca Naruto."
    )