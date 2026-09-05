from fastapi.testclient import TestClient

from main import app
from models import Produto, Categoria

client = TestClient(app)


def test_visualizar_pedido_inexistente(db):
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

    response = client.get(
        "/pedidos/999",
        headers=headers
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Pedido não encontrado."


def test_usuario_nao_pode_visualizar_pedido_de_outro_usuario(db):
    
    client.post(
        "/usuarios",
        json={
            "name": "Pedro",
            "email": "pedro@teste.com",
            "password": "Pedro123@"
        }
    )

    login_pedro = client.post(
        "/usuarios/login",
        json={
            "email": "pedro@teste.com",
            "password": "Pedro123@"
        }
    )

    token_pedro = login_pedro.json()["access_token"]

    headers_pedro = {
        "Authorization": f"Bearer {token_pedro}"
    }

    categoria = Categoria(name="Geek")

    db.add(categoria)
    db.commit()
    db.refresh(categoria)

    produto = Produto(
        name="Caneca Naruto",
        price=50,
        estoque=10,
        category_id=categoria.id
    )

    db.add(produto)
    db.commit()
    db.refresh(produto)

    client.post(
        "/carrinho",
        json={
            "produto_id": produto.id,
            "quantidade": 2
        },
        headers=headers_pedro
    )

    pedido = client.post(
        "/pedidos",
        headers=headers_pedro
    )

    pedido_id = pedido.json()["id"]
    
    client.post(
        "/usuarios",
        json={
            "name": "Maria",
            "email": "maria@teste.com",
            "password": "Maria123@"
        }
    )

    login_maria = client.post(
        "/usuarios/login",
        json={
            "email": "maria@teste.com",
            "password": "Maria123@"
        }
    )

    token_maria = login_maria.json()["access_token"]

    headers_maria = {
        "Authorization": f"Bearer {token_maria}"
    }

    # Maria tenta acessar o pedido de Pedro
    response = client.get(
        f"/pedidos/{pedido_id}",
        headers=headers_maria
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Pedido não encontrado."