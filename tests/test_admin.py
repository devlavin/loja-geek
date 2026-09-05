from fastapi.testclient import TestClient

from main import app
from models import user, category, product, order
from sqlalchemy import select

client = TestClient(app)

def test_user_nao_pode_list_orders_admin(db):
    response = client.post(
        "/users",
        json={
            "name": "Pedro",
            "email": "pedro@teste.com",
            "password": "Pedro123@"
        }
    )

    assert response.status_code == 200

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
        "/admin/orders",
        headers=headers
    )

    assert response.status_code == 403
    
def create_order_para_admin(db, admin_token):
    response = client.post(
        "/users",
        json={
            "name": "Pedro",
            "email": "pedro@teste.com",
            "password": "Pedro123@"
        }
    )

    assert response.status_code == 200

    login = client.post(
        "/users/login",
        json={
            "email": "pedro@teste.com",
            "password": "Pedro123@"
        }
    )

    token = login.json()["access_token"]

    headers_user = {
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
        headers=headers_user
    )

    assert response.status_code == 200

    response = client.post(
        "/orders",
        headers=headers_user
    )

    assert response.status_code == 200

    order_id = response.json()["id"]

    headers_admin = {
        "Authorization": f"Bearer {admin_token}"
    }

    return headers_admin, order_id, product
    
def test_admin_list_todos_orders(db, admin_token):
    headers, order_id, product = create_order_para_admin(
        db,
        admin_token
    )

    response = client.get(
        "/admin/orders",
        headers=headers
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["id"] == order_id
    assert data[0]["user_id"] is not None
    assert data[0]["status"] == "PENDENTE"

    assert len(data[0]["items"]) == 1
    assert data[0]["items"][0]["product_id"] == product.id
    assert data[0]["items"][0]["name"] == "Caneca Naruto"
    assert data[0]["items"][0]["quantity"] == 2
    assert data[0]["items"][0]["preco"] == 50.0
    assert data[0]["items"][0]["subtotal"] == 100.0

    assert data[0]["total"] == 100.0
    
def test_admin_get_order_inexistente(
    db,
    admin_token
):
    headers = {
        "Authorization": f"Bearer {admin_token}"
    }

    response = client.get(
        "/admin/orders/999999",
        headers=headers
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "order não encontrado."
    
def test_admin_alterar_status_pendente_para_pago(
    db,
    admin_token
):
    headers, order_id, product = create_order_para_admin(
        db,
        admin_token
    )

    response = client.patch(
        f"/admin/orders/{order_id}/status",
        json={
            "status": "PAGO"
        },
        headers=headers
    )

    assert response.status_code == 200

    data = response.json()

    assert data["message"] == "Status atualizado com sucesso."
    assert data["order_id"] == order_id
    assert data["status"] == "PAGO"

def test_admin_nao_pode_pular_status(
    db,
    admin_token
):
    headers, order_id, product = create_order_para_admin(
        db,
        admin_token
    )

    response = client.patch(
        f"/admin/orders/{order_id}/status",
        json={
            "status": "ENVIADO"
        },
        headers=headers
    )

    assert response.status_code == 400

    assert response.json()["detail"] == (
        "Não é possível alterar o order de "
        "PENDENTE para ENVIADO."
    )
    
def test_admin_status_invalido(
    db,
    admin_token
):
    headers, order_id, product = create_order_para_admin(
        db,
        admin_token
    )

    response = client.patch(
        f"/admin/orders/{order_id}/status",
        json={
            "status": "QUALQUER_COISA"
        },
        headers=headers
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Status inválido."
    
def test_admin_alterar_status_order_inexistente(
    db,
    admin_token
):
    headers = {
        "Authorization": f"Bearer {admin_token}"
    }

    response = client.patch(
        "/admin/orders/999999/status",
        json={
            "status": "PAGO"
        },
        headers=headers
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "order não encontrado."
    
def test_admin_list_users(db, admin_token):
    response = client.post(
        "/users",
        json={
            "name": "Pedro",
            "email": "pedro@teste.com",
            "password": "Pedro123@"
        }
    )

    assert response.status_code == 200

    headers = {
        "Authorization": f"Bearer {admin_token}"
    }

    response = client.get(
        "/admin/users",
        headers=headers
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 2

    emails = [user["email"] for user in data]

    assert "pedro@teste.com" in emails
    assert "admin@test.com" in emails
    
def test_admin_get_user(db, admin_token):
    response = client.post(
        "/users",
        json={
            "name": "Pedro",
            "email": "pedro@teste.com",
            "password": "Pedro123@"
        }
    )

    assert response.status_code == 200

    resultado = db.execute(
        select(user).where(
            user.email == "pedro@teste.com"
        )
    )

    user = resultado.scalar_one()

    headers = {
        "Authorization": f"Bearer {admin_token}"
    }

    response = client.get(
        f"/admin/users/{user.id}",
        headers=headers
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == user.id
    assert data["name"] == "Pedro"
    assert data["email"] == "pedro@teste.com"
    assert data["role"] == "user"
    
def test_admin_get_user_inexistente(
    db,
    admin_token
):
    headers = {
        "Authorization": f"Bearer {admin_token}"
    }

    response = client.get(
        "/admin/users/999999",
        headers=headers
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Usuário não encontrado."
    
def test_admin_promover_user(
    db,
    admin_token
):
    response = client.post(
        "/users",
        json={
            "name": "Pedro",
            "email": "pedro@teste.com",
            "password": "Pedro123@"
        }
    )

    assert response.status_code == 200

    resultado = db.execute(
        select(user).where(
            user.email == "pedro@teste.com"
        )
    )

    user = resultado.scalar_one()

    headers = {
        "Authorization": f"Bearer {admin_token}"
    }

    response = client.patch(
        f"/admin/users/{user.id}/role",
        params={
            "role": "admin"
        },
        headers=headers
    )

    assert response.status_code == 200

    data = response.json()

    assert data["message"] == "Role atualizada com sucesso."
    assert data["user_id"] == user.id
    assert data["role"] == "admin"

    db.refresh(user)

    assert user.role == "admin"
    
def test_admin_rebaixar_user(
    db,
    admin_token
):
    response = client.post(
        "/users",
        json={
            "name": "Pedro",
            "email": "pedro@teste.com",
            "password": "Pedro123@"
        }
    )

    assert response.status_code == 200

    resultado = db.execute(
        select(user).where(
            user.email == "pedro@teste.com"
        )
    )

    user = resultado.scalar_one()

    user.role = "admin"
    db.commit()

    headers = {
        "Authorization": f"Bearer {admin_token}"
    }

    response = client.patch(
        f"/admin/users/{user.id}/role",
        params={
            "role": "user"
        },
        headers=headers
    )

    assert response.status_code == 200

    data = response.json()

    assert data["role"] == "user"

    db.refresh(user)

    assert user.role == "user"
    
def test_admin_role_invalida(
    db,
    admin_token
):
    response = client.post(
        "/users",
        json={
            "name": "Pedro",
            "email": "pedro@teste.com",
            "password": "Pedro123@"
        }
    )

    assert response.status_code == 200

    resultado = db.execute(
        select(user).where(
            user.email == "pedro@teste.com"
        )
    )

    user = resultado.scalar_one()

    headers = {
        "Authorization": f"Bearer {admin_token}"
    }

    response = client.patch(
        f"/admin/users/{user.id}/role",
        params={
            "role": "superadmin"
        },
        headers=headers
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Role inválida."
    
def test_admin_nao_pode_remover_propria_role(
    db,
    admin_token
):
    resultado = db.execute(
        select(user).where(
            user.email == "admin@test.com"
        )
    )

    admin = resultado.scalar_one()

    headers = {
        "Authorization": f"Bearer {admin_token}"
    }

    response = client.patch(
        f"/admin/users/{admin.id}/role",
        params={
            "role": "user"
        },
        headers=headers
    )

    assert response.status_code == 400

    assert response.json()["detail"] == (
        "Você não pode remover sua própria "
        "permissão de administrador."
    )