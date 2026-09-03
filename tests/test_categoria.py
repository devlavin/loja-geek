from fastapi.testclient import TestClient

from main import app
from models import Produto, Categoria

client = TestClient(app)

def test_listar_categorias():
    response = client.get("/categorias")
    
    assert response.status_code == 200
    
def test_criar_categoria_no_banco(admin_token, db):
    
    headers = {
        "Authorization": f"Bearer {admin_token}"
    }
    
    response = client.post(
        f"/categorias",
        json={
                "name": "Jogos"
            },
            headers = headers
    )
    
    assert response.status_code == 200
    
def test_buscar_categoria(admin_token, db):
    categoria = Categoria(
        name = "Jogos"
    )
    
    db.add(categoria)
    db.commit()
    db.refresh(categoria)
    
    headers = {
        "Authorization": f"Bearer {admin_token}"
    }
    
    response = client.get(
        f"/categorias/{categoria.id}",
        headers = headers
    )
    
    assert response.status_code == 200
    
def test_atualizar_categoria(admin_token, db):
    categoria = Categoria(
        name = "Chaveiros"
    )
    
    db.add(categoria)
    db.commit()
    db.refresh(categoria)
    
    headers = {
        "Authorization": f"Bearer {admin_token}"
    }
    
    response = client.patch(
        f"/categorias/{categoria.id}",
        json = {
            "name": "Chaveirinhos"
        },
        headers = headers
    )
    
    assert response.status_code == 200
    
def test_deletar_categoria(admin_token, db):
    categoria = Categoria(
        name = "Filmes"
    )
    
    db.add(categoria)
    db.commit()
    db.refresh(categoria)
    
    headers = {
        "Authorization": f"Bearer {admin_token}"
    }
    
    response = client.delete(
        f"/categorias/{categoria.id}",
        headers = headers
    )
    
    assert response.status_code == 200
    
    categoria_excluida = db.query(Categoria).filter(
        Categoria.id == categoria.id
    ).first()
    
    assert categoria_excluida is None
    
def test_nao_deletar_categoria_com_produtos(admin_token, db):
    categoria = Categoria(
        name = "Chinelo"
    )
    
    db.add(categoria)
    db.commit()
    db.refresh(categoria)
    
    produto = Produto(
        name = "Chinelo Sonserina",
        price = 99.99,
        estoque = 25,
        category_id = categoria.id
    )
    
    db.add(produto)
    db.commit()
    db.refresh(produto)
    
    headers = {
        "Authorization": f"Bearer {admin_token}"
    }
    
    response = client.delete(
        f"/categorias/{categoria.id}",
        headers = headers
    )
    
    
    assert response.status_code == 400
    
    categoria_excluida = db.query(Categoria).filter(
        Categoria.id == categoria.id
    ).first()
    
    assert categoria_excluida is not None
    
    