from fastapi.testclient import TestClient

from main import app
from models import Product, Category

client = TestClient(app)


def create_order_for_test(db):
    response = client.post(
        "/users",
        json={
            "name": "Pedro",
            "email": "pedro@teste.com",
            "password": "Pedro123@"
        }
    )

    assert response.status_code == 200

    login = client.post(
        "/users/login",
        json={
            "email": "pedro@teste.com",
            "password": "Pedro123@"
        }
    )

    assert login.status_code == 200

    token = login.json()["access_token"]

    headers = {
        "Authorization": f"Bearer {token}"
    }

    category = Category(name="Geek")

    db.add(category)
    db.commit()
    db.refresh(category)

    product = Product(
        name="Caneca Naruto",
        price=50,
        stock=10,
        category_id=category.id
    )

    db.add(product)
    db.commit()
    db.refresh(product)

    response = client.post(
        "/cart",
        json={
            "product_id": product.id,
            "quantity": 2
        },
        headers=headers
    )

    assert response.status_code == 200

    order = client.post(
        "/orders",
        headers=headers
    )

    assert order.status_code == 200

    order_id = order.json()["id"]

    return headers, order_id


def test_pay_order(db):
    headers, order_id = create_order_for_test(db)

    response = client.post(
        f"/orders/{order_id}/pay",
        headers=headers
    )

    assert response.status_code == 200

    data = response.json()

    assert data["message"] == "Pagamento aprovado."
    assert data["order_id"] == order_id
    assert data["status"] == "PAGO"


def test_pay_already_paid_order(db):
    headers, order_id = create_order_for_test(db)

    # First payment
    response = client.post(
        f"/orders/{order_id}/pay",
        headers=headers
    )

    assert response.status_code == 200

    # Second payment
    response = client.post(
        f"/orders/{order_id}/pay",
        headers=headers
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Este pedido não pode ser pago."


def test_pay_nonexistent_order(db):
    headers, _ = create_order_for_test(db)

    response = client.post(
        "/orders/999/pay",
        headers=headers
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Pedido não encontrado."


def test_user_cannot_pay_another_users_order(db):
    _, order_id = create_order_for_test(db)

    response = client.post(
        "/users",
        json={
            "name": "Maria",
            "email": "maria@teste.com",
            "password": "Maria123@"
        }
    )

    assert response.status_code == 200

    login = client.post(
        "/users/login",
        json={
            "email": "maria@teste.com",
            "password": "Maria123@"
        }
    )

    assert login.status_code == 200

    token_maria = login.json()["access_token"]

    headers_maria = {
        "Authorization": f"Bearer {token_maria}"
    }

    # Maria tries to pay Pedro's order
    response = client.post(
        f"/orders/{order_id}/pay",
        headers=headers_maria
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Pedido não encontrado."