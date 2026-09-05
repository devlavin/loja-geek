from fastapi.testclient import TestClient

from main import app
from models import Usuario, Categoria, Produto, Pedido
from sqlalchemy import select

client = TestClient(app)

def test_usuario_nao_pode_listar_pedidos_admin(db):
    response = client.post(
        "/usuarios",
        json={
            "name": "Pedro",
            "email": "pedro@teste.com",
            "password": "Pedro123@"
        }
    )

    assert response.status_code == 200

    login = client.post(
        "/usuarios/login",
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
        "/admin/pedidos",
        headers=headers
    )

    assert response.status_code == 403
    
def criar_pedido_para_admin(db, admin_token):
    response = client.post(
        "/usuarios",
        json={
            "name": "Pedro",
            "email": "pedro@teste.com",
            "password": "Pedro123@"
        }
    )

    assert response.status_code == 200

    login = client.post(
        "/usuarios/login",
        json={
            "email": "pedro@teste.com",
            "password": "Pedro123@"
        }
    )

    token = login.json()["access_token"]

    headers_usuario = {
        "Authorization": f"Bearer {token}"
    }

    categoria = Categoria(
        name="Geek"
    )

    db.add(categoria)
    db.commit()
    db.refresh(categoria)

    produto = Produto(
        name="Caneca Naruto",
        price=50,
        estoque=10,
        category_id=categoria.id
    )

    db.add(produto)
    db.commit()
    db.refresh(produto)

    response = client.post(
        "/carrinho",
        json={
            "produto_id": produto.id,
            "quantidade": 2
        },
        headers=headers_usuario
    )

    assert response.status_code == 200

    response = client.post(
        "/pedidos",
        headers=headers_usuario
    )

    assert response.status_code == 200

    pedido_id = response.json()["id"]

    headers_admin = {
        "Authorization": f"Bearer {admin_token}"
    }

    return headers_admin, pedido_id, produto
    
def test_admin_listar_todos_pedidos(db, admin_token):
    headers, pedido_id, produto = criar_pedido_para_admin(
        db,
        admin_token
    )

    response = client.get(
        "/admin/pedidos",
        headers=headers
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["id"] == pedido_id
    assert data[0]["usuario_id"] is not None
    assert data[0]["status"] == "PENDENTE"

    assert len(data[0]["itens"]) == 1
    assert data[0]["itens"][0]["produto_id"] == produto.id
    assert data[0]["itens"][0]["nome"] == "Caneca Naruto"
    assert data[0]["itens"][0]["quantidade"] == 2
    assert data[0]["itens"][0]["preco"] == 50.0
    assert data[0]["itens"][0]["subtotal"] == 100.0

    assert data[0]["total"] == 100.0
    
def test_admin_visualizar_pedido_inexistente(
    db,
    admin_token
):
    headers = {
        "Authorization": f"Bearer {admin_token}"
    }

    response = client.get(
        "/admin/pedidos/999999",
        headers=headers
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Pedido não encontrado."
    
def test_admin_alterar_status_pendente_para_pago(
    db,
    admin_token
):
    headers, pedido_id, produto = criar_pedido_para_admin(
        db,
        admin_token
    )

    response = client.patch(
        f"/admin/pedidos/{pedido_id}/status",
        json={
            "status": "PAGO"
        },
        headers=headers
    )

    assert response.status_code == 200

    data = response.json()

    assert data["message"] == "Status atualizado com sucesso."
    assert data["pedido_id"] == pedido_id
    assert data["status"] == "PAGO"

def test_admin_nao_pode_pular_status(
    db,
    admin_token
):
    headers, pedido_id, produto = criar_pedido_para_admin(
        db,
        admin_token
    )

    response = client.patch(
        f"/admin/pedidos/{pedido_id}/status",
        json={
            "status": "ENVIADO"
        },
        headers=headers
    )

    assert response.status_code == 400

    assert response.json()["detail"] == (
        "Não é possível alterar o pedido de "
        "PENDENTE para ENVIADO."
    )
    
def test_admin_status_invalido(
    db,
    admin_token
):
    headers, pedido_id, produto = criar_pedido_para_admin(
        db,
        admin_token
    )

    response = client.patch(
        f"/admin/pedidos/{pedido_id}/status",
        json={
            "status": "QUALQUER_COISA"
        },
        headers=headers
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Status inválido."
    
def test_admin_alterar_status_pedido_inexistente(
    db,
    admin_token
):
    headers = {
        "Authorization": f"Bearer {admin_token}"
    }

    response = client.patch(
        "/admin/pedidos/999999/status",
        json={
            "status": "PAGO"
        },
        headers=headers
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Pedido não encontrado."
    
def test_admin_listar_usuarios(db, admin_token):
    response = client.post(
        "/usuarios",
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
        "/admin/usuarios",
        headers=headers
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 2

    emails = [usuario["email"] for usuario in data]

    assert "pedro@teste.com" in emails
    assert "admin@test.com" in emails
    
def test_admin_visualizar_usuario(db, admin_token):
    response = client.post(
        "/usuarios",
        json={
            "name": "Pedro",
            "email": "pedro@teste.com",
            "password": "Pedro123@"
        }
    )

    assert response.status_code == 200

    resultado = db.execute(
        select(Usuario).where(
            Usuario.email == "pedro@teste.com"
        )
    )

    usuario = resultado.scalar_one()

    headers = {
        "Authorization": f"Bearer {admin_token}"
    }

    response = client.get(
        f"/admin/usuarios/{usuario.id}",
        headers=headers
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == usuario.id
    assert data["name"] == "Pedro"
    assert data["email"] == "pedro@teste.com"
    assert data["role"] == "user"
    
def test_admin_visualizar_usuario_inexistente(
    db,
    admin_token
):
    headers = {
        "Authorization": f"Bearer {admin_token}"
    }

    response = client.get(
        "/admin/usuarios/999999",
        headers=headers
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Usuário não encontrado."
    
def test_admin_promover_usuario(
    db,
    admin_token
):
    response = client.post(
        "/usuarios",
        json={
            "name": "Pedro",
            "email": "pedro@teste.com",
            "password": "Pedro123@"
        }
    )

    assert response.status_code == 200

    resultado = db.execute(
        select(Usuario).where(
            Usuario.email == "pedro@teste.com"
        )
    )

    usuario = resultado.scalar_one()

    headers = {
        "Authorization": f"Bearer {admin_token}"
    }

    response = client.patch(
        f"/admin/usuarios/{usuario.id}/role",
        params={
            "role": "admin"
        },
        headers=headers
    )

    assert response.status_code == 200

    data = response.json()

    assert data["message"] == "Role atualizada com sucesso."
    assert data["usuario_id"] == usuario.id
    assert data["role"] == "admin"

    db.refresh(usuario)

    assert usuario.role == "admin"
    
def test_admin_rebaixar_usuario(
    db,
    admin_token
):
    response = client.post(
        "/usuarios",
        json={
            "name": "Pedro",
            "email": "pedro@teste.com",
            "password": "Pedro123@"
        }
    )

    assert response.status_code == 200

    resultado = db.execute(
        select(Usuario).where(
            Usuario.email == "pedro@teste.com"
        )
    )

    usuario = resultado.scalar_one()

    usuario.role = "admin"
    db.commit()

    headers = {
        "Authorization": f"Bearer {admin_token}"
    }

    response = client.patch(
        f"/admin/usuarios/{usuario.id}/role",
        params={
            "role": "user"
        },
        headers=headers
    )

    assert response.status_code == 200

    data = response.json()

    assert data["role"] == "user"

    db.refresh(usuario)

    assert usuario.role == "user"
    
def test_admin_role_invalida(
    db,
    admin_token
):
    response = client.post(
        "/usuarios",
        json={
            "name": "Pedro",
            "email": "pedro@teste.com",
            "password": "Pedro123@"
        }
    )

    assert response.status_code == 200

    resultado = db.execute(
        select(Usuario).where(
            Usuario.email == "pedro@teste.com"
        )
    )

    usuario = resultado.scalar_one()

    headers = {
        "Authorization": f"Bearer {admin_token}"
    }

    response = client.patch(
        f"/admin/usuarios/{usuario.id}/role",
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
        select(Usuario).where(
            Usuario.email == "admin@test.com"
        )
    )

    admin = resultado.scalar_one()

    headers = {
        "Authorization": f"Bearer {admin_token}"
    }

    response = client.patch(
        f"/admin/usuarios/{admin.id}/role",
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