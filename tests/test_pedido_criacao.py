from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_create_order_with_empty_cart(user_headers):
    response = client.post(
        "/orders",
        headers=user_headers
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Carrinho vazio."


def test_create_order_with_insufficient_stock(
    db,
    user_headers,
    product
):
    product.stock = 1
    db.commit()

    response = client.post(
        "/cart",
        json={
            "product_id": product.id,
            "quantity": 1
        },
        headers=user_headers
    )

    assert response.status_code == 200

    product.stock = 0
    db.commit()

    response = client.post(
        "/orders",
        headers=user_headers
    )

    assert response.status_code == 400
    assert response.json()["detail"] == (
        "Estoque insuficiente para o produto: Caneca Naruto."
    )