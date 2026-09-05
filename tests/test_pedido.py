from fastapi.testclient import TestClient

from main import app
from models import Produto, Categoria, Carrinho, Usuario
from sqlalchemy import select

client = TestClient(app)

def test_criar_pedido(db):
    response = client.post(
        "/usuarios",
        json={
            "name": "Pedro",
            "email": "pedro@teste.com",
            "password": "Pedro123@"
        }
    )
    
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
        headers=headers
    )

    assert response.status_code == 200
    
    response = client.post(
        "/pedidos",
        headers=headers
    )

    assert response.status_code == 200
    
    data = response.json()
    
    assert data["status"] == "PENDENTE"
    assert len(data["itens"]) == 1
    assert data["itens"][0]["produto_id"] == produto.id
    assert data["itens"][0]["quantidade"] == 2
    assert data["itens"][0]["preco"] == "50.00"
    assert data["itens"][0]["subtotal"] == "100.00"
    assert data["total"] == "100.00"
    
    # Verifica estoque
    db.refresh(produto)

    assert produto.estoque == 8

    # Verifica se o carrinho foi esvaziado
    resultado = db.execute(
        select(Usuario).where(
            Usuario.email == "pedro@teste.com"
        )
    )

    usuario = resultado.scalar_one()

    resultado = db.execute(
        select(Carrinho).where(
            Carrinho.usuario_id == usuario.id
        )
    )

    carrinho = resultado.scalar_one()

    assert len(carrinho.itens) == 0
    
def test_ver_pedidos(db):
    response = client.post(
        "/usuarios",
        json={
            "name": "Pedro",
            "email": "pedro@teste.com",
            "password": "Pedro123@"
        }
    )
        
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
        headers=headers
    )
    
    assert response.status_code == 200
    
    response = client.post(
        "/pedidos",
        headers=headers
    )

    assert response.status_code == 200
    
    response = client.get(
        "/pedidos",
        headers=headers
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["status"] == "PENDENTE"
    assert data[0]["itens"][0]["produto_id"] == produto.id
    assert data[0]["itens"][0]["quantidade"] == 2
    assert data[0]["total"] == "100.00"
    
def test_visualizar_pedido(db):
    response = client.post(
        "/usuarios",
        json={
            "name": "Pedro Hall",
            "email": "pedro@teste.com",
            "password": "Pedro123@"
        }
    )
    
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
    
    categoria = Categoria(
        name = "Distopic"
    )
    
    db.add(categoria)
    db.commit()
    db.refresh(categoria)
    
    produto = Produto(
        name = "Box Divergente",
        price = 214.99,
        estoque = 8,
        category_id = categoria.id
    )
    
    db.add(produto)
    db.commit()
    db.refresh(produto)
    
    response = client.post(
        "/carrinho/",
        json={
            "produto_id": produto.id,
            "quantidade": 1
        },
        headers = headers
    )
    
    assert response.status_code == 200
    
    response = client.post(
        "/pedidos",
        headers=headers
    )

    assert response.status_code == 200
    
    data = response.json()

    pedido_id = data["id"]
    
    response = client.get(
        f"/pedidos/{pedido_id}",
        headers = headers
    )
    
    assert response.status_code == 200
    
    data = response.json()
    
    assert data["id"] == pedido_id
    assert data["status"] == "PENDENTE"
    assert len(data["itens"]) == 1
    assert data["itens"][0]["produto_id"] == produto.id
    assert data["itens"][0]["nome"] == "Box Divergente"
    assert data["itens"][0]["quantidade"] == 1
    assert data["itens"][0]["preco"] == "214.99"
    assert data["itens"][0]["subtotal"] == "214.99"
    assert data["total"] == "214.99"