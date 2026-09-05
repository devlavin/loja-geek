from fastapi.testclient import TestClient

from main import app
from models import product, category

client = TestClient(app)


def test_create_order_com_cart_vazio(db):
    
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

    response = client.post(
        "/orders",
        headers=headers
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "cart vazio."


def test_create_order_com_stock_insuficiente(db):

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
        "stock insuficiente para o product: Caneca Naruto."
    )