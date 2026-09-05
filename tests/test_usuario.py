from fastapi.testclient import TestClient

from main import app
from models import Usuario

client = TestClient(app)

def test_criar_usuario():

    response = client.post(
        f"/usuarios",
        json={
            "name": "Pedro Hall",
            "email": "pedro@teste.com",
            "password": "Pedro123@"
        }
    )
    
    print(response.json())
    
    assert response.status_code == 200

def test_criar_usuario_email_invalido():

    response = client.post(
        f"/usuarios",
        json={
            "name": "Pedro Hall",
            "email": "pedro_teste.com",
            "password": "Pedro123@"
        }
    )
    
    assert response.status_code == 422

def test_criar_usuario_com_senha_invalida():

    response = client.post(
        f"/usuarios",
        json={
            "name": "Pedro Hall",
            "email": "pedro@teste.com",
            "password": "pedro123"
        }
    )
    
    assert response.status_code == 422
    
def test_criar_usuario_duplicado(db):
    usuario = Usuario(
        name = "Pedro Hall",
        email = "pedro@teste.com",
        password_hash = "Pedro123@"
    )
    
    db.add(usuario)
    db.commit()
    db.refresh(usuario)

    response = client.post(
        f"/usuarios",
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
        "/usuarios",
        json={
            "name": "Pedro Hall",
            "email": "pedro@teste.com",
            "password": "Pedro123@"
        }
    )
    
    response = client.post(
        f"/usuarios/login",
        json={
            "email": "pedro@teste.com",
            "password": "Pedro123@"
        }
    )
    
    assert response.status_code == 200
    
    dados = response.json()

    assert "access_token" in dados
    assert dados["token_type"] == "bearer"

def test_login_senha_invalida():
    client.post(
        "/usuarios",
        json={
            "name": "Pedro Hall",
            "email": "pedro@teste.com",
            "password": "Pedro123@"
        }
    )
    
    response = client.post(
        f"/usuarios/login",
        json={
            "email": "pedro@teste.com",
            "password": "pedro123"
        }
    )
    
    assert response.status_code == 401

def test_usuario_atual():
    client.post(
    "/usuarios",
        json={
            "name": "Pedro Hall",
            "email": "pedro@teste.com",
            "password": "Pedro123@"
        }
    )
    
    response = client.post(
        f"/usuarios/login",
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
        f"/usuarios/me",
        headers = headers
    )
    
    assert response.status_code == 200
    
    dados = response.json()
    
    assert dados ["name"] == "Pedro Hall"
    assert dados ["email"] == "pedro@teste.com"

def test_atualizar_email():
    response = client.post(
        "/usuarios",
        json={
            "name": "Pedro",
            "email": "pedro@email.com",
            "password": "Pedro123@"
        }
    )

    usuario = response.json()

    login = client.post(
        "/usuarios/login",
        json={
            "email": "pedro@email.com",
            "password": "Pedro123@"
        }
    )

    token = login.json()["access_token"]

    response = client.patch(
        f"/usuarios/{usuario['id']}",
        json={
            "email": "pedronovo@email.com"
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200
    assert response.json()["email"] == "pedronovo@email.com"
    
def test_atualizar_senha():
    response = client.post(
        "/usuarios",
        json={
            "name": "Pedro",
            "email": "pedro@email.com",
            "password": "Pedro123@"
        }
    )

    usuario = response.json()

    login = client.post(
        "/usuarios/login",
        json={
            "email": "pedro@email.com",
            "password": "Pedro123@"
        }
    )

    token = login.json()["access_token"]

    response = client.patch(
        f"/usuarios/{usuario['id']}",
        json={
            "password": "Pedro123!"
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200

    login_novo = client.post(
        "/usuarios/login",
        json={
            "email": "pedro@email.com",
            "password": "Pedro123!"
        }
    )

    assert login_novo.status_code == 200
    
def test_deletar_usuario():
    response = client.post(
        "/usuarios",
        json={
            "name": "Pedro",
            "email": "pedro@email.com",
            "password": "Pedro123@"
        }
    )

    usuario = response.json()

    login = client.post(
        "/usuarios/login",
        json={
            "email": "pedro@email.com",
            "password": "Pedro123@"
        }
    )

    token = login.json()["access_token"]

    response = client.delete(
        f"/usuarios/{usuario['id']}",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200
    
    login_depois = client.post(
        "/usuarios/login",
        json={
            "email": "pedro@email.com",
            "password": "Pedro123@"
        }
    )

    assert login_depois.status_code == 401