from fastapi.testclient import TestClient

from main import app
from models import product, category

client = TestClient(app)

def test_list_products():
    response = client.get("/products")
    
    assert response.status_code == 200
    
def test_buscar_product(admin_token, db):
    category = category(
        name = "Chinelo"
    )
    
    db.add(category)
    db.commit()
    db.refresh(category)
    
    product = product(
        name = "Chinelo Grifinoria",
        price = 99.99,
        stock = 14,
        category_id = category.id
    )
    
    db.add(product)
    db.commit()
    db.refresh(product)
    
    headers = {
        "Authorization": f"Bearer {admin_token}"
    }
    
    response = client.get(
        f"/products/{product.id}",
        headers = headers
        
    )
    
    assert response.status_code == 200   
        
    
def test_create_product_no_banco(db):
    category = category(
        name="category Teste"
    )

    db.add(category)
    db.commit()
    db.refresh(category)
    
    product = product(
        name="Camiseta Teste",
        price = 39.99,
        stock = 10,
        category_id = category.id
    )
    
    db.add(product)
    db.commit()
    db.refresh(product)
    
    assert product.id is not None
    assert product.name == "Camiseta Teste"
    assert product.stock == 10
    assert product.category_id == category.id
    
def test_create_product(admin_token, db):
    category = category(
        name="Harry Potter"
    )
    
    db.add(category)
    db.commit()
    db.refresh(category)
    
    headers = {
        "Authorization": f"Bearer {admin_token}"
    }

    response = client.post(
        f"/products",
        json=[
            {
                "name": "Camiseta Corvinal",
                "price": 49.99,
                "stock": 8,
                "category_id": category.id
            }
        ],
        headers=headers
    )

    assert response.status_code == 200
    
def test_update_preco(admin_token, db):
    category = category(
        name="Jogos Vorazes"
    )
    
    db.add(category)
    db.commit()
    db.refresh(category)
    
    product = product(
        name="Caneca Snow",
        price=35.89,
        stock=5,
        category_id=category.id
    )

    db.add(product)
    db.commit()
    db.refresh(product)
    
    headers = {
        "Authorization": f"Bearer {admin_token}"
    }
    
    response = client.patch(
        f"/products/{product.id}",
        json={
            "price": 39.99
        },
        headers = headers
    )
    
    assert response.status_code == 200
    
def test_update_stock(admin_token, db):
    category = category(
        name="Maze Runner"
    )
    
    db.add(category)
    db.commit()
    db.refresh(category)
    
    product = product(
        name="Maze Runner: Correr ou Morrer",
        price = 45.79,
        stock = 12,
        category_id = category.id
    )
    
    db.add(product)
    db.commit()
    db.refresh(product)
    
    headers = {
        "Authorization": f"Bearer {admin_token}"
    }
    
    response = client.patch(
        f"/products/{product.id}/stock",
        json={
            "stock": 15
        },
        headers = headers
    )
    
    assert response.status_code == 200
    
def test_delete_product(admin_token, db):
    category = category(
        name="Percy Jackson"
    )
    
    db.add(category)
    db.commit()
    db.refresh(category)
    
    product = product(
        name = "Camiseta Tridente Poseidon",
        price = 57.99,
        stock = 5,
        category_id = category.id
    )
    
    db.add(product)
    db.commit()
    db.refresh(product)
    
    headers = {
        "Authorization": f"Bearer {admin_token}"
    }
    
    response = client.delete(
        f"/products/{product.id}",
        headers = headers
    )
    
    assert response.status_code == 200
    
    product_excluido = db.query(product).filter(
        product.id == product.id
    ).first()
    
    assert product_excluido is None