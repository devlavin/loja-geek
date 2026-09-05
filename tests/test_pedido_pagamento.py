from fastapi.testclient import TestClient

from main import app
from models import product, category

client = TestClient(app)


def create_order_teste(db):

    client.post(
        "/users",
        json={
            "name": "Pedro",
            "email": "pedro@teste.com",
            "password": "Pedro123@"
        }
    )

    login = client.post(
        "/users/login",
        json={
            "email": "pedro@teste.com",
            "password": "Pedro123@"
        }
    )

    token = login.json()["access_token"]

    headers = {
        "Authorization": f"Bearer {token}"
    }

    category = category(name="Geek")

    db.add(category)
    db.commit()
    db.refresh(category)

    product = product(
        name="Caneca Naruto",
        price=50,
        stock=10,
        category_id=category.id
    )

    db.add(product)
    db.commit()
    db.refresh(product)

    client.post(
        "/cart",
        json={
            "product_id": product.id,
            "quantity": 2
        },
        headers=headers
    )

    order = client.post(
        "/orders",
        headers=headers
    )

    order_id = order.json()["id"]

    return headers, order_id


def test_pay_order(db):
    headers, order_id = create_order_teste(db)

    response = client.post(
        f"/orders/{order_id}/pay",
        headers=headers
    )

    assert response.status_code == 200

    data = response.json()

    assert data["message"] == "Pagamento aprovado."
    assert data["order_id"] == order_id
    assert data["status"] == "PAGO"


def test_pay_order_ja_pago(db):
    headers, order_id = create_order_teste(db)

    # Primeiro pagamento
    response = client.post(
        f"/orders/{order_id}/pay",
        headers=headers
    )

    assert response.status_code == 200

    # Segundo pagamento
    response = client.post(
        f"/orders/{order_id}/pay",
        headers=headers
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Este order não pode ser pago."


def test_pay_order_inexistente(db):
    headers, _ = create_order_teste(db)

    response = client.post(
        "/orders/999/pay",
        headers=headers
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "order não encontrado."


def test_user_nao_pode_pay_order_de_outro_user(db):
    headers_pedro, order_id = create_order_teste(db)

    client.post(
        "/users",
        json={
            "name": "Maria",
            "email": "maria@teste.com",
            "password": "Maria123@"
        }
    )

    login = client.post(
        "/users/login",
        json={
            "email": "maria@teste.com",
            "password": "Maria123@"
        }
    )

    token_maria = login.json()["access_token"]

    headers_maria = {
        "Authorization": f"Bearer {token_maria}"
    }

    # Maria tenta pay o order de Pedro
    response = client.post(
        f"/orders/{order_id}/pay",
        headers=headers_maria
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "order não encontrado."