from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_get_nonexistent_order(user_headers):
    response = client.get(
        "/orders/999",
        headers=user_headers
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Pedido não encontrado."


def test_user_cannot_get_another_users_order(
    user_headers,
    product
):
    response = client.post(
        "/cart",
        json={
            "product_id": product.id,
            "quantity": 2
        },
        headers=user_headers
    )

    assert response.status_code == 200

    order = client.post(
        "/orders",
        json={
            "phone": "16999999999",
            "delivery_type": "retirada",
            "payment_method": "pix"
        },
        headers=user_headers
    )

    assert order.status_code == 200

    order_id = order.json()["id"]

    # Create another user
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