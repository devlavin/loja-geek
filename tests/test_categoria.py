from fastapi.testclient import TestClient

from main import app
from models import product, category

client = TestClient(app)

def test_list_categorys():
    response = client.get("/categorys")
    
    assert response.status_code == 200
    
def test_create_category_no_banco(admin_token, db):
    
    headers = {
        "Authorization": f"Bearer {admin_token}"
    }
    
    response = client.post(
        f"/categorys",
        json={
                "name": "Jogos"
            },
            headers = headers
    )
    
    assert response.status_code == 200
    
def test_buscar_category(admin_token, db):
    category = category(
        name = "Jogos"
    )
    
    db.add(category)
    db.commit()
    db.refresh(category)
    
    headers = {
        "Authorization": f"Bearer {admin_token}"
    }
    
    response = client.get(
        f"/categorys/{category.id}",
        headers = headers
    )
    
    assert response.status_code == 200
    
def test_update_category(admin_token, db):
    category = category(
        name = "Chaveiros"
    )
    
    db.add(category)
    db.commit()
    db.refresh(category)
    
    headers = {
        "Authorization": f"Bearer {admin_token}"
    }
    
    response = client.patch(
        f"/categorys/{category.id}",
        json = {
            "name": "Chaveirinhos"
        },
        headers = headers
    )
    
    assert response.status_code == 200
    
def test_deletar_category(admin_token, db):
    category = category(
        name = "Filmes"
    )
    
    db.add(category)
    db.commit()
    db.refresh(category)
    
    headers = {
        "Authorization": f"Bearer {admin_token}"
    }
    
    response = client.delete(
        f"/categorys/{category.id}",
        headers = headers
    )
    
    assert response.status_code == 200
    
    category_excluida = db.query(category).filter(
        category.id == category.id
    ).first()
    
    assert category_excluida is None
    
def test_nao_deletar_category_com_products(admin_token, db):
    category = category(
        name = "Chinelo"
    )
    
    db.add(category)
    db.commit()
    db.refresh(category)
    
    product = product(
        name = "Chinelo Sonserina",
        price = 99.99,
        stock = 25,
        category_id = category.id
    )
    
    db.add(product)
    db.commit()
    db.refresh(product)
    
    headers = {
        "Authorization": f"Bearer {admin_token}"
    }
    
    response = client.delete(
        f"/categorys/{category.id}",
        headers = headers
    )
    
    
    assert response.status_code == 400
    
    category_excluida = db.query(category).filter(
        category.id == category.id
    ).first()
    
    assert category_excluida is not None
    
    