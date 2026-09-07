from fastapi.testclient import TestClient

from main import app
from models import Category, Product

client = TestClient(app)


def test_create_order_with_empty_cart(db):
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

    token = login.json()["access_token"]

    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = client.post(
        "/orders",
        headers=headers
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Carrinho vazio."


def test_create_order_with_insufficient_stock(db):
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
        stock=1,
        category_id=category.id
    )

    db.add(product)
    db.commit()
    db.refresh(product)

    response = client.post(
        "/cart",
        json={
            "product_id": product.id,
            "quantity": 1
        },
        headers=headers
    )

    assert response.status_code == 200

    product.stock = 0
    db.commit()

    response = client.post(
        "/orders",
        headers=headers
    )

    assert response.status_code == 400
    assert response.json()["detail"] == (
        "Estoque insuficiente para o produto: Caneca Naruto."
    )