from fastapi.testclient import TestClient

from main import app
from models import user

client = TestClient(app)

def test_create_user():

    response = client.post(
        f"/users",
        json={
            "name": "Pedro Hall",
            "email": "pedro@teste.com",
            "password": "Pedro123@"
        }
    )
    
    print(response.json())
    
    assert response.status_code == 200

def test_create_user_email_invalido():

    response = client.post(
        f"/users",
        json={
            "name": "Pedro Hall",
            "email": "pedro_teste.com",
            "password": "Pedro123@"
        }
    )
    
    assert response.status_code == 422

def test_create_user_com_password_invalida():

    response = client.post(
        f"/users",
        json={
            "name": "Pedro Hall",
            "email": "pedro@teste.com",
            "password": "pedro123"
        }
    )
    
    assert response.status_code == 422
    
def test_create_user_duplicado(db):
    user = user(
        name = "Pedro Hall",
        email = "pedro@teste.com",
        password_hash = "Pedro123@"
    )
    
    db.add(user)
    db.commit()
    db.refresh(user)

    response = client.post(
        f"/users",
        json={
            "name": "Pedro Hall",
            "email": "pedro@teste.com",
            "password": "Pedro123@"
        }
    )
    
    print(response.json())
    
    assert response.status_code == 400
    
def test_login():
    client.post(
        "/users",
        json={
            "name": "Pedro Hall",
            "email": "pedro@teste.com",
            "password": "Pedro123@"
        }
    )
    
    response = client.post(
        f"/users/login",
        json={
            "email": "pedro@teste.com",
            "password": "Pedro123@"
        }
    )
    
    assert response.status_code == 200
    
    dados = response.json()

    assert "access_token" in dados
    assert dados["token_type"] == "bearer"

def test_login_password_invalida():
    client.post(
        "/users",
        json={
            "name": "Pedro Hall",
            "email": "pedro@teste.com",
            "password": "Pedro123@"
        }
    )
    
    response = client.post(
        f"/users/login",
        json={
            "email": "pedro@teste.com",
            "password": "pedro123"
        }
    )
    
    assert response.status_code == 401

def test_user_atual():
    client.post(
    "/users",
        json={
            "name": "Pedro Hall",
            "email": "pedro@teste.com",
            "password": "Pedro123@"
        }
    )
    
    response = client.post(
        f"/users/login",
        json={
            "email": "pedro@teste.com",
            "password": "Pedro123@"
        }
    )
    
    dados =response.json()
    token = dados["access_token"]
    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    response = client.get(
        f"/users/me",
        headers = headers
    )
    
    assert response.status_code == 200
    
    dados = response.json()
    
    assert dados ["name"] == "Pedro Hall"
    assert dados ["email"] == "pedro@teste.com"

def test_update_email():
    response = client.post(
        "/users",
        json={
            "name": "Pedro",
            "email": "pedro@email.com",
            "password": "Pedro123@"
        }
    )

    user = response.json()

    login = client.post(
        "/users/login",
        json={
            "email": "pedro@email.com",
            "password": "Pedro123@"
        }
    )

    token = login.json()["access_token"]

    response = client.patch(
        f"/users/{user['id']}",
        json={
            "email": "pedronovo@email.com"
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200
    assert response.json()["email"] == "pedronovo@email.com"
    
def test_update_password():
    response = client.post(
        "/users",
        json={
            "name": "Pedro",
            "email": "pedro@email.com",
            "password": "Pedro123@"
        }
    )

    user = response.json()

    login = client.post(
        "/users/login",
        json={
            "email": "pedro@email.com",
            "password": "Pedro123@"
        }
    )

    token = login.json()["access_token"]

    response = client.patch(
        f"/users/{user['id']}",
        json={
            "password": "Pedro123!"
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200

    login_novo = client.post(
        "/users/login",
        json={
            "email": "pedro@email.com",
            "password": "Pedro123!"
        }
    )

    assert login_novo.status_code == 200
    
def test_deletar_user():
    response = client.post(
        "/users",
        json={
            "name": "Pedro",
            "email": "pedro@email.com",
            "password": "Pedro123@"
        }
    )

    user = response.json()

    login = client.post(
        "/users/login",
        json={
            "email": "pedro@email.com",
            "password": "Pedro123@"
        }
    )

    token = login.json()["access_token"]

    response = client.delete(
        f"/users/{user['id']}",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200
    
    login_depois = client.post(
        "/users/login",
        json={
            "email": "pedro@email.com",
            "password": "Pedro123@"
        }
    )

    assert login_depois.status_code == 401