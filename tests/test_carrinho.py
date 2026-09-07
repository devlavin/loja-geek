from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_add_product_to_cart(user_headers, product):
    response = client.post(
        "/cart",
        json={
            "product_id": product.id,
            "quantity": 2
        },
        headers=user_headers
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data["items"]) == 1
    assert data["items"][0]["product_id"] == product.id
    assert data["items"][0]["quantity"] == 2
    assert data["items"][0]["price"] == "50.00"
    assert data["items"][0]["subtotal"] == "100.00"
    assert data["total"] == "100.00"


def test_cannot_add_quantity_greater_than_stock(db, user_headers, product):
    product.stock = 5
    db.commit()

    response = client.post(
        "/cart",
        json={
            "product_id": product.id,
            "quantity": 6
        },
        headers=user_headers
    )

    assert response.status_code == 400
    assert response.json()["detail"] == (
        "Quantidade solicitada maior que o estoque disponível."
    )


def test_add_nonexistent_product_to_cart(user_headers):
    response = client.post(
        "/cart",
        json={
            "product_id": 9999,
            "quantity": 1
        },
        headers=user_headers
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Produto não encontrado."


def test_add_product_without_stock(db, user_headers, product):
    product.stock = 0
    db.commit()

    response = client.post(
        "/cart",
        json={
            "product_id": product.id,
            "quantity": 1
        },
        headers=user_headers
    )

    assert response.status_code == 400
    assert response.json()["detail"] == (
        "Quantidade solicitada maior que o estoque disponível."
    )


def test_cannot_add_duplicate_product_to_cart(user_headers, product):
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
        "/cart",
        json={
            "product_id": product.id,
            "quantity": 1
        },
        headers=user_headers
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Produto já está no carrinho."


def test_get_cart(user_headers, product):
    response = client.post(
        "/cart",
        json={
            "product_id": product.id,
            "quantity": 2
        },
        headers=user_headers
    )

    assert response.status_code == 200

    response = client.get(
        "/cart",
        headers=user_headers
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data["items"]) == 1

    item = data["items"][0]

    assert item["product_id"] == product.id
    assert item["name"] == "Caneca Naruto"
    assert item["price"] == "50.00"
    assert item["quantity"] == 2
    assert item["subtotal"] == "100.00"

    assert data["total"] == "100.00"


def test_update_cart_quantity(user_headers, product):
    response = client.post(
        "/cart",
        json={
            "product_id": product.id,
            "quantity": 2
        },
        headers=user_headers
    )

    assert response.status_code == 200

    response = client.patch(
        f"/cart/{product.id}",
        params={
            "quantity": 5
        },
        headers=user_headers
    )

    assert response.status_code == 200

    data = response.json()

    assert data["product_id"] == product.id
    assert data["quantity"] == 5


def test_update_cart_quantity_to_zero(user_headers, product):
    client.post(
        "/cart",
        json={
            "product_id": product.id,
            "quantity": 2
        },
        headers=user_headers
    )

    response = client.patch(
        f"/cart/{product.id}",
        params={
            "quantity": 0
        },
        headers=user_headers
    )

    assert response.status_code == 400
    assert response.json()["detail"] == (
        "A quantidade deve ser maior que zero."
    )


def test_update_cart_quantity_greater_than_stock(
    db,
    user_headers,
    product
):
    product.stock = 5
    db.commit()

    response = client.post(
        "/cart",
        json={
            "product_id": product.id,
            "quantity": 2
        },
        headers=user_headers
    )

    assert response.status_code == 200

    response = client.patch(
        f"/cart/{product.id}",
        params={
            "quantity": 6
        },
        headers=user_headers
    )

    assert response.status_code == 400
    assert response.json()["detail"] == (
        "Quantidade solicitada maior que o estoque disponível."
    )


def test_update_product_not_in_cart(user_headers, product):
    client.get(
        "/cart",
        headers=user_headers
    )

    response = client.patch(
        f"/cart/{product.id}",
        params={
            "quantity": 5
        },
        headers=user_headers
    )

    assert response.status_code == 404
    assert response.json()["detail"] == (
        "Produto não está no carrinho."
    )


def test_remove_product_from_cart(user_headers, product):
    response = client.post(
        "/cart",
        json={
            "product_id": product.id,
            "quantity": 2
        },
        headers=user_headers
    )

    assert response.status_code == 200

    response = client.delete(
        f"/cart/{product.id}",
        headers=user_headers
    )

    assert response.status_code == 200
    assert response.json()["message"] == (
        "Produto removido do carrinho."
    )

    response = client.get(
        "/cart",
        headers=user_headers
    )

    assert response.status_code == 200
    assert response.json()["items"] == []
    assert response.json()["total"] == "0"


def test_remove_product_not_in_cart(user_headers, product):
    client.get(
        "/cart",
        headers=user_headers
    )

    response = client.delete(
        f"/cart/{product.id}",
        headers=user_headers
    )

    assert response.status_code == 404
    assert response.json()["detail"] == (
        "Produto não está no carrinho."
    )


def test_get_empty_cart(user_headers):
    response = client.get(
        "/cart",
        headers=user_headers
    )

    assert response.status_code == 200

    data = response.json()

    assert data["items"] == []
    assert data["total"] == "0"