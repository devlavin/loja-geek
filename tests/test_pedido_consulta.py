from fastapi.testclient import TestClient

from main import app
from models import Category, Product

client = TestClient(app)


def test_get_nonexistent_order(db):
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

    response = client.get(
        "/orders/999",
        headers=headers
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Pedido não encontrado."


def test_user_cannot_get_another_users_order(db):
    response = client.post(
        "/users",
        json={
            "name": "Pedro",
            "email": "pedro@teste.com",
            "password": "Pedro123@"
        }
    )

    assert response.status_code == 200

    login_pedro = client.post(
        "/users/login",
        json={
            "email": "pedro@teste.com",
            "password": "Pedro123@"
        }
    )

    assert login_pedro.status_code == 200

    token_pedro = login_pedro.json()["access_token"]

    headers_pedro = {
        "Authorization": f"Bearer {token_pedro}"
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
        headers=headers_pedro
    )

    assert response.status_code == 200

    order = client.post(
        "/orders",
        headers=headers_pedro
    )

    assert order.status_code == 200

    order_id = order.json()["id"]

    response = client.post(
        "/users",
        json={
            "name": "Maria",
            "email": "maria@teste.com",
            "password": "Maria123@"
        }
    )

    assert response.status_code == 200

    login_maria = client.post(
        "/users/login",
        json={
            "email": "maria@teste.com",
            "password": "Maria123@"
        }
    )

    assert login_maria.status_code == 200

    token_maria = login_maria.json()["access_token"]

    headers_maria = {
        "Authorization": f"Bearer {token_maria}"
    }

    # Maria tries to access Pedro's order
    response = client.get(
        f"/orders/{order_id}",
        headers=headers_maria
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Pedido não encontrado."