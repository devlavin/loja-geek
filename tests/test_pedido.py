from fastapi.testclient import TestClient

from main import app
from models import product, category, cart, user
from sqlalchemy import select

client = TestClient(app)

def test_create_order(db):
    response = client.post(
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
    
    category = category(
        name="Geek"
    )

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
    
    response = client.post(
        "/cart",
        json={
            "product_id": product.id,
            "quantity": 2
        },
        headers=headers
    )

    assert response.status_code == 200
    
    response = client.post(
        "/orders",
        headers=headers
    )

    assert response.status_code == 200
    
    data = response.json()
    
    assert data["status"] == "PENDENTE"
    assert len(data["items"]) == 1
    assert data["items"][0]["product_id"] == product.id
    assert data["items"][0]["quantity"] == 2
    assert data["items"][0]["preco"] == "50.00"
    assert data["items"][0]["subtotal"] == "100.00"
    assert data["total"] == "100.00"
    
    # Verifica stock
    db.refresh(product)

    assert product.stock == 8

    # Verifica se o cart foi esvaziado
    resultado = db.execute(
        select(user).where(
            user.email == "pedro@teste.com"
        )
    )

    user = resultado.scalar_one()

    resultado = db.execute(
        select(cart).where(
            cart.user_id == user.id
        )
    )

    cart = resultado.scalar_one()

    assert len(cart.items) == 0
    
def test_ver_orders(db):
    response = client.post(
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
    
    category = category(
            name="Geek"
        )
    
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
    
    response = client.post(
        "/cart",
        json={
            "product_id": product.id,
            "quantity": 2
        },
        headers=headers
    )
    
    assert response.status_code == 200
    
    response = client.post(
        "/orders",
        headers=headers
    )

    assert response.status_code == 200
    
    response = client.get(
        "/orders",
        headers=headers
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["status"] == "PENDENTE"
    assert data[0]["items"][0]["product_id"] == product.id
    assert data[0]["items"][0]["quantity"] == 2
    assert data[0]["total"] == "100.00"
    
def test_get_order(db):
    response = client.post(
        "/users",
        json={
            "name": "Pedro Hall",
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
    
    category = category(
        name = "Distopic"
    )
    
    db.add(category)
    db.commit()
    db.refresh(category)
    
    product = product(
        name = "Box Divergente",
        price = 214.99,
        stock = 8,
        category_id = category.id
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
        headers = headers
    )
    
    assert response.status_code == 200
    
    response = client.post(
        "/orders",
        headers=headers
    )

    assert response.status_code == 200
    
    data = response.json()

    order_id = data["id"]
    
    response = client.get(
        f"/orders/{order_id}",
        headers = headers
    )
    
    assert response.status_code == 200
    
    data = response.json()
    
    assert data["id"] == order_id
    assert data["status"] == "PENDENTE"
    assert len(data["items"]) == 1
    assert data["items"][0]["product_id"] == product.id
    assert data["items"][0]["name"] == "Box Divergente"
    assert data["items"][0]["quantity"] == 1
    assert data["items"][0]["preco"] == "214.99"
    assert data["items"][0]["subtotal"] == "214.99"
    assert data["total"] == "214.99"