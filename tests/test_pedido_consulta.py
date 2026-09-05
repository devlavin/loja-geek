from fastapi.testclient import TestClient

from main import app
from models import product, category

client = TestClient(app)


def test_get_order_inexistente(db):
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

    response = client.get(
        "/orders/999",
        headers=headers
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "order não encontrado."


def test_user_nao_pode_get_order_de_outro_user(db):
    
    client.post(
        "/users",
        json={
            "name": "Pedro",
            "email": "pedro@teste.com",
            "password": "Pedro123@"
        }
    )

    login_pedro = client.post(
        "/users/login",
        json={
            "email": "pedro@teste.com",
            "password": "Pedro123@"
        }
    )

    token_pedro = login_pedro.json()["access_token"]

    headers_pedro = {
        "Authorization": f"Bearer {token_pedro}"
    }

    category = category(name="Geek")

    db.add(category)
    db.commit()
    db.refresh(category)

    product = product(
        name="Caneca Naruto",
        price=50,
        stock=10,
        category_id=category.id
    )

    db.add(product)
    db.commit()
    db.refresh(product)

    client.post(
        "/cart",
        json={
            "product_id": product.id,
            "quantity": 2
        },
        headers=headers_pedro
    )

    order = client.post(
        "/orders",
        headers=headers_pedro
    )

    order_id = order.json()["id"]
    
    client.post(
        "/users",
        json={
            "name": "Maria",
            "email": "maria@teste.com",
            "password": "Maria123@"
        }
    )

    login_maria = client.post(
        "/users/login",
        json={
            "email": "maria@teste.com",
            "password": "Maria123@"
        }
    )

    token_maria = login_maria.json()["access_token"]

    headers_maria = {
        "Authorization": f"Bearer {token_maria}"
    }

    # Maria tenta acessar o order de Pedro
    response = client.get(
        f"/orders/{order_id}",
        headers=headers_maria
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "order não encontrado."