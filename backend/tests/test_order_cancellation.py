from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def create_order_for_test(user_headers, product):
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

    return order.json()["id"]


def test_cancel_pending_order(db, user_headers, product):
    order_id = create_order_for_test(user_headers, product)

    db.refresh(product)

    assert product.stock == 8

    response = client.patch(
        f"/orders/{order_id}/cancel",
        headers=user_headers
    )

    assert response.status_code == 200

    db.refresh(product)

    assert product.stock == 10

    data = response.json()

    assert data["message"] == "Pedido cancelado com sucesso."
    assert data["order_id"] == order_id
    assert data["status"] == "CANCELADO"


def test_cancel_paid_order(db, user_headers, product):
    order_id = create_order_for_test(user_headers, product)

    response = client.post(
        f"/orders/{order_id}/pay",
        headers=user_headers
    )

    assert response.status_code == 200

    response = client.patch(
        f"/orders/{order_id}/cancel",
        headers=user_headers
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "CANCELADO"

    # Stock should be restored
    db.refresh(product)

    assert product.stock == 10


def test_cancel_already_cancelled_order(user_headers, product):
    order_id = create_order_for_test(user_headers, product)

    response = client.patch(
        f"/orders/{order_id}/cancel",
        headers=user_headers
    )

    assert response.status_code == 200

    response = client.patch(
        f"/orders/{order_id}/cancel",
        headers=user_headers
    )

    assert response.status_code == 400
    assert response.json()["detail"] == (
        "Este pedido não pode ser cancelado."
    )


def test_cancel_nonexistent_order(user_headers, product):
    create_order_for_test(user_headers, product)

    response = client.patch(
        "/orders/999/cancel",
        headers=user_headers
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Pedido não encontrado."


def test_user_cannot_cancel_another_users_order(
    user_headers,
    product
):
    order_id = create_order_for_test(user_headers, product)

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

    # Maria tries to cancel Pedro's order
    response = client.patch(
        f"/orders/{order_id}/cancel",
        headers=headers_maria
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Pedido não encontrado."