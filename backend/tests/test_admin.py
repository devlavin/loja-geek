from fastapi.testclient import TestClient

from sqlalchemy import select

from main import app
from models import User, Category, Product

client = TestClient(app)


def create_order_for_admin(user_headers, product):
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
        "/orders",
        json={
            "phone": "16999999999",
            "delivery_type": "retirada",
            "payment_method": "pix"
        },
        headers=user_headers
    )

    assert response.status_code == 200

    return response.json()["id"]


def test_user_cannot_list_admin_orders(user_headers):
    response = client.get(
        "/admin/orders",
        headers=user_headers
    )

    assert response.status_code == 403


def test_admin_list_all_orders(
    admin_headers,
    user_headers,
    product
):
    order_id = create_order_for_admin(
        user_headers,
        product
    )

    response = client.get(
        "/admin/orders",
        headers=admin_headers
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
    assert data[0]["items"][0]["price"] == 50.0
    assert data[0]["items"][0]["subtotal"] == 100.0

    assert data[0]["total"] == 100.0


def test_admin_get_nonexistent_order(admin_headers):
    response = client.get(
        "/admin/orders/999999",
        headers=admin_headers
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Pedido não encontrado."


def test_admin_update_order_status_pending_to_paid(
    admin_headers,
    user_headers,
    product
):
    order_id = create_order_for_admin(
        user_headers,
        product
    )

    response = client.patch(
        f"/admin/orders/{order_id}/status",
        json={
            "status": "PAGO"
        },
        headers=admin_headers
    )

    assert response.status_code == 200

    data = response.json()

    assert data["message"] == "Status atualizado com sucesso."
    assert data["order_id"] == order_id
    assert data["status"] == "PAGO"


def test_admin_cannot_skip_order_status(
    admin_headers,
    user_headers,
    product
):
    order_id = create_order_for_admin(
        user_headers,
        product
    )

    response = client.patch(
        f"/admin/orders/{order_id}/status",
        json={
            "status": "ENVIADO"
        },
        headers=admin_headers
    )

    assert response.status_code == 400
    assert response.json()["detail"] == (
        "Não é possível alterar o pedido de "
        "PENDENTE para ENVIADO."
    )


def test_admin_invalid_order_status(
    admin_headers,
    user_headers,
    product
):
    order_id = create_order_for_admin(
        user_headers,
        product
    )

    response = client.patch(
        f"/admin/orders/{order_id}/status",
        json={
            "status": "QUALQUER_COISA"
        },
        headers=admin_headers
    )

    assert response.status_code == 422


def test_admin_update_nonexistent_order_status(admin_headers):
    response = client.patch(
        "/admin/orders/999999/status",
        json={
            "status": "PAGO"
        },
        headers=admin_headers
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Pedido não encontrado."


def test_admin_list_users(admin_headers):
    response = client.post(
        "/users",
        json={
            "name": "Pedro",
            "email": "pedro@teste.com",
            "password": "Pedro123@"
        }
    )

    assert response.status_code == 200

    response = client.get(
        "/admin/users",
        headers=admin_headers
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 2

    emails = [user["email"] for user in data]

    assert "pedro@teste.com" in emails
    assert "admin@test.com" in emails


def test_admin_get_user(admin_headers, db):
    response = client.post(
        "/users",
        json={
            "name": "Pedro",
            "email": "pedro@teste.com",
            "password": "Pedro123@"
        }
    )

    assert response.status_code == 200

    result = db.execute(
        select(User).where(
            User.email == "pedro@teste.com"
        )
    )

    user = result.scalar_one()

    response = client.get(
        f"/admin/users/{user.id}",
        headers=admin_headers
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == user.id
    assert data["name"] == "Pedro"
    assert data["email"] == "pedro@teste.com"
    assert data["role"] == "user"


def test_admin_get_nonexistent_user(admin_headers):
    response = client.get(
        "/admin/users/999999",
        headers=admin_headers
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Usuário não encontrado."


def test_admin_promote_user(admin_headers, db):
    response = client.post(
        "/users",
        json={
            "name": "Pedro",
            "email": "pedro@teste.com",
            "password": "Pedro123@"
        }
    )

    assert response.status_code == 200

    result = db.execute(
        select(User).where(
            User.email == "pedro@teste.com"
        )
    )

    user = result.scalar_one()

    response = client.patch(
        f"/admin/users/{user.id}/role",
        json={"role": "admin"},
        headers=admin_headers
    )
    
    assert response.status_code == 200

    data = response.json()

    assert data["message"] == "Role atualizada com sucesso."
    assert data["user_id"] == user.id
    assert data["role"] == "admin"

    db.refresh(user)

    assert user.role == "admin"


def test_admin_demote_user(admin_headers, db):
    response = client.post(
        "/users",
        json={
            "name": "Pedro",
            "email": "pedro@teste.com",
            "password": "Pedro123@"
        }
    )

    assert response.status_code == 200

    result = db.execute(
        select(User).where(
            User.email == "pedro@teste.com"
        )
    )

    user = result.scalar_one()

    user.role = "admin"
    db.commit()

    response = client.patch(
        f"/admin/users/{user.id}/role",
        json={
            "role": "user"
        },
        headers=admin_headers
    )

    assert response.status_code == 200

    data = response.json()

    assert data["role"] == "user"

    db.refresh(user)

    assert user.role == "user"


def test_admin_invalid_role(admin_headers, db):
    response = client.post(
        "/users",
        json={
            "name": "Pedro",
            "email": "pedro@teste.com",
            "password": "Pedro123@"
        }
    )

    assert response.status_code == 200

    result = db.execute(
        select(User).where(
            User.email == "pedro@teste.com"
        )
    )

    user = result.scalar_one()

    response = client.patch(
        f"/admin/users/{user.id}/role",
        json={
            "role": "superadmin"
        },
        headers=admin_headers
    )

    assert response.status_code == 422


def test_admin_cannot_remove_own_admin_role(
    admin_headers,
    db
):
    result = db.execute(
        select(User).where(
            User.email == "admin@test.com"
        )
    )

    admin = result.scalar_one()

    response = client.patch(
        f"/admin/users/{admin.id}/role",
        json={
            "role": "user"
        },
        headers=admin_headers
    )

    assert response.status_code == 400
    assert response.json()["detail"] == (
        "Você não pode remover sua própria "
        "permissão de administrador."
    )