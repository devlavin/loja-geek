from fastapi.testclient import TestClient
from sqlalchemy import select

from main import app
from models import Cart, User

client = TestClient(app)


def test_create_order(db, user_headers, product):
    response = client.post(
        "/cart",
        json={
            "product_id": product.id,
            "quantity": 2
        },
        headers=user_headers
    )

    assert response.status_code == 200

    response = client.post(
        "/orders",
        headers=user_headers
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "PENDENTE"
    assert len(data["items"]) == 1
    assert data["items"][0]["product_id"] == product.id
    assert data["items"][0]["quantity"] == 2
    assert data["items"][0]["price"] == "50.00"
    assert data["items"][0]["subtotal"] == "100.00"
    assert data["total"] == "100.00"

    # Check stock
    db.refresh(product)

    assert product.stock == 8

    # Check if cart was emptied
    result = db.execute(
        select(User).where(
            User.email == "pedro@teste.com"
        )
    )

    user = result.scalar_one()

    result = db.execute(
        select(Cart).where(
            Cart.user_id == user.id
        )
    )

    cart = result.scalar_one()

    assert len(cart.items) == 0


def test_list_orders(user_headers, product):
    response = client.post(
        "/cart",
        json={
            "product_id": product.id,
            "quantity": 2
        },
        headers=user_headers
    )

    assert response.status_code == 200

    response = client.post(
        "/orders",
        headers=user_headers
    )

    assert response.status_code == 200

    response = client.get(
        "/orders",
        headers=user_headers
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["status"] == "PENDENTE"
    assert data[0]["items"][0]["product_id"] == product.id
    assert data[0]["items"][0]["quantity"] == 2
    assert data[0]["total"] == "100.00"


def test_get_order(user_headers, db, category):
    # Esse teste precisa de um produto específico,
    # então criamos ele usando a fixture de categoria.
    from models import Product

    product = Product(
        name="Box Divergente",
        price=214.99,
        stock=8,
        category_id=category.id
    )

    db.add(product)
    db.commit()
    db.refresh(product)

    response = client.post(
        "/cart/",
        json={
            "product_id": product.id,
            "quantity": 1
        },
        headers=user_headers
    )

    assert response.status_code == 200

    response = client.post(
        "/orders",
        headers=user_headers
    )

    assert response.status_code == 200

    data = response.json()

    order_id = data["id"]

    response = client.get(
        f"/orders/{order_id}",
        headers=user_headers
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == order_id
    assert data["status"] == "PENDENTE"
    assert len(data["items"]) == 1
    assert data["items"][0]["product_id"] == product.id
    assert data["items"][0]["name"] == "Box Divergente"
    assert data["items"][0]["quantity"] == 1
    assert data["items"][0]["price"] == "214.99"
    assert data["items"][0]["subtotal"] == "214.99"
    assert data["total"] == "214.99"