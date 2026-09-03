from fastapi.testclient import TestClient

from main import app
from models import Produto, Categoria

client = TestClient(app)

def test_listar_produtos():
    response = client.get("/produtos")
    
    assert response.status_code == 200
    
def test_buscar_produto(admin_token, db):
    categoria = Categoria(
        name = "Chinelo"
    )
    
    db.add(categoria)
    db.commit()
    db.refresh(categoria)
    
    produto = Produto(
        name = "Chinelo Grifinoria",
        price = 99.99,
        estoque = 14,
        category_id = categoria.id
    )
    
    db.add(produto)
    db.commit()
    db.refresh(produto)
    
    headers = {
        "Authorization": f"Bearer {admin_token}"
    }
    
    response = client.get(
        f"/produtos/{produto.id}",
        headers = headers
        
    )
    
    assert response.status_code == 200   
        
    
def test_criar_produto_no_banco(db):
    categoria = Categoria(
        name="Categoria Teste"
    )

    db.add(categoria)
    db.commit()
    db.refresh(categoria)
    
    produto = Produto(
        name="Camiseta Teste",
        price = 39.99,
        estoque = 10,
        category_id = categoria.id
    )
    
    db.add(produto)
    db.commit()
    db.refresh(produto)
    
    assert produto.id is not None
    assert produto.name == "Camiseta Teste"
    assert produto.estoque == 10
    assert produto.category_id == categoria.id
    
def test_cadastrar_produto(admin_token, db):
    categoria = Categoria(
        name="Harry Potter"
    )
    
    db.add(categoria)
    db.commit()
    db.refresh(categoria)
    
    headers = {
        "Authorization": f"Bearer {admin_token}"
    }

    response = client.post(
        f"/produtos",
        json=[
            {
                "name": "Camiseta Corvinal",
                "price": 49.99,
                "estoque": 8,
                "category_id": categoria.id
            }
        ],
        headers=headers
    )

    assert response.status_code == 200
    
def test_atualizar_preco(admin_token, db):
    categoria = Categoria(
        name="Jogos Vorazes"
    )
    
    db.add(categoria)
    db.commit()
    db.refresh(categoria)
    
    produto = Produto(
        name="Caneca Snow",
        price=35.89,
        estoque=5,
        category_id=categoria.id
    )

    db.add(produto)
    db.commit()
    db.refresh(produto)
    
    headers = {
        "Authorization": f"Bearer {admin_token}"
    }
    
    response = client.patch(
        f"/produtos/{produto.id}",
        json={
            "price": 39.99
        },
        headers = headers
    )
    
    assert response.status_code == 200
    
def test_atualizar_estoque(admin_token, db):
    categoria = Categoria(
        name="Maze Runner"
    )
    
    db.add(categoria)
    db.commit()
    db.refresh(categoria)
    
    produto = Produto(
        name="Maze Runner: Correr ou Morrer",
        price = 45.79,
        estoque = 12,
        category_id = categoria.id
    )
    
    db.add(produto)
    db.commit()
    db.refresh(produto)
    
    headers = {
        "Authorization": f"Bearer {admin_token}"
    }
    
    response = client.patch(
        f"/produtos/{produto.id}/estoque",
        json={
            "estoque": 15
        },
        headers = headers
    )
    
    assert response.status_code == 200
    
def test_delete_produto(admin_token, db):
    categoria = Categoria(
        name="Percy Jackson"
    )
    
    db.add(categoria)
    db.commit()
    db.refresh(categoria)
    
    produto = Produto(
        name = "Camiseta Tridente Poseidon",
        price = 57.99,
        estoque = 5,
        category_id = categoria.id
    )
    
    db.add(produto)
    db.commit()
    db.refresh(produto)
    
    headers = {
        "Authorization": f"Bearer {admin_token}"
    }
    
    response = client.delete(
        f"/produtos/{produto.id}",
        headers = headers
    )
    
    assert response.status_code == 200
    
    produto_excluido = db.query(Produto).filter(
        Produto.id == produto.id
    ).first()
    
    assert produto_excluido is None