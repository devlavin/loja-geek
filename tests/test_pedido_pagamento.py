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
        headers=user_headers
    )

    assert order.status_code == 200

    return order.json()["id"]


def test_pay_order(user_headers, product):
    order_id = create_order_for_test(user_headers, product)

    response = client.post(
        f"/orders/{order_id}/pay",
        headers=user_headers
    )

    assert response.status_code == 200

    data = response.json()

    assert data["message"] == "Pagamento aprovado."
    assert data["order_id"] == order_id
    assert data["status"] == "PAGO"


def test_pay_already_paid_order(user_headers, product):
    order_id = create_order_for_test(user_headers, product)

    response = client.post(
        f"/orders/{order_id}/pay",
        headers=user_headers
    )

    assert response.status_code == 200

    response = client.post(
        f"/orders/{order_id}/pay",
        headers=user_headers
    )

    assert response.status_code == 400
    assert response.json()["detail"] == (
        "Este pedido não pode ser pago."
    )


def test_pay_nonexistent_order(user_headers, product):
    create_order_for_test(user_headers, product)

    response = client.post(
        "/orders/999/pay",
        headers=user_headers
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Pedido não encontrado."


def test_user_cannot_pay_another_users_order(
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

    response = client.post(
        f"/orders/{order_id}/pay",
        headers=headers_maria
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Pedido não encontrado."