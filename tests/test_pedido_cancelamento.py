from fastapi.testclient import TestClient

from main import app
from models import Produto, Categoria

client = TestClient(app)


def criar_pedido_teste(db):
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
        headers=headers
    )

    pedido = client.post(
        "/pedidos",
        headers=headers
    )

    pedido_id = pedido.json()["id"]

    return headers, pedido_id, produto


def test_cancelar_pedido_pendente(db):
    headers, pedido_id, produto = criar_pedido_teste(db)
    
    db.refresh(produto)

    assert produto.estoque == 8

    response = client.patch(
        f"/pedidos/{pedido_id}/cancelar",
        headers=headers
    )

    assert response.status_code == 200
    
    db.refresh(produto)

    assert produto.estoque == 10

    data = response.json()

    assert data["message"] == "Pedido cancelado com sucesso."
    assert data["pedido_id"] == pedido_id
    assert data["status"] == "CANCELADO"


def test_cancelar_pedido_pago(db):
    headers, pedido_id, produto = criar_pedido_teste(db)

    response = client.post(
        f"/pedidos/{pedido_id}/pagar",
        headers=headers
    )

    assert response.status_code == 200

    response = client.patch(
        f"/pedidos/{pedido_id}/cancelar",
        headers=headers
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "CANCELADO"

    # Estoque volta
    db.refresh(produto)

    assert produto.estoque == 10


def test_cancelar_pedido_ja_cancelado(db):
    headers, pedido_id, _ = criar_pedido_teste(db)

    response = client.patch(
        f"/pedidos/{pedido_id}/cancelar",
        headers=headers
    )

    assert response.status_code == 200

    response = client.patch(
        f"/pedidos/{pedido_id}/cancelar",
        headers=headers
    )

    assert response.status_code == 400
    assert response.json()["detail"] == (
        "Este pedido não pode ser cancelado."
    )


def test_cancelar_pedido_inexistente(db):
    headers, _, _ = criar_pedido_teste(db)

    response = client.patch(
        "/pedidos/999/cancelar",
        headers=headers
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Pedido não encontrado."


def test_usuario_nao_pode_cancelar_pedido_de_outro_usuario(db):
    headers_pedro, pedido_id, _ = criar_pedido_teste(db)

    client.post(
        "/usuarios",
        json={
            "name": "Maria",
            "email": "maria@teste.com",
            "password": "Maria123@"
        }
    )

    login = client.post(
        "/usuarios/login",
        json={
            "email": "maria@teste.com",
            "password": "Maria123@"
        }
    )

    token_maria = login.json()["access_token"]

    headers_maria = {
        "Authorization": f"Bearer {token_maria}"
    }

    # Maria tenta cancelar pedido de Pedro
    response = client.patch(
        f"/pedidos/{pedido_id}/cancelar",
        headers=headers_maria
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Pedido não encontrado."