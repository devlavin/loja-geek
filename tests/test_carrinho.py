from fastapi.testclient import TestClient

from main import app
from models import category, product

client = TestClient(app)

def test_adicionar_product_cart(db):

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
    
    category = category(
        name="Canecas"
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
        headers=headers
    )

    assert response.status_code == 200

    dados = response.json()

    assert len(dados["items"]) == 1
    assert dados["items"][0]["product_id"] == product.id
    assert dados["items"][0]["quantity"] == 2
    assert dados["items"][0]["preco"] == "50.00"
    assert dados["items"][0]["subtotal"] == "100.00"
    assert dados["total"] == "100.00"
    
def test_nao_adicionar_quantity_maior_que_stock(db):

    response = client.post(
        "/users",
        json={
            "name": "Pedro",
            "email": "pedro@teste.com",
            "password": "Pedro123@"
        }
    )

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

    category = category(
        name="Canecas"
    )

    db.add(category)
    db.commit()
    db.refresh(category)

    product = product(
        name="Caneca Naruto",
        price=50,
        stock=5,
        category_id=category.id
    )

    db.add(product)
    db.commit()
    db.refresh(product)

    response = client.post(
        "/cart",
        json={
            "product_id": product.id,
            "quantity": 6
        },
        headers=headers
    )

    assert response.status_code == 400
    assert response.json()["detail"] == (
        "quantity solicitada maior que o stock disponível."
    )

def test_adicionar_product_inexistente():

    response = client.post(
        "/users",
        json={
            "name": "Pedro",
            "email": "pedro@teste.com",
            "password": "Pedro123@"
        }
    )

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

    response = client.post(
        "/cart",
        json={
            "product_id": 9999,
            "quantity": 1
        },
        headers=headers
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "product não encontrado."
    
def test_adicionar_product_sem_stock(db):

    client.post(
        "/users",
        json={
            "name": "Pedro",
            "email": "pedro@teste.com",
            "password": "Pedro123@"
        }
    )

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

    category = category(
        name="Canecas"
    )

    db.add(category)
    db.commit()
    db.refresh(category)

    product = product(
        name="Caneca Naruto",
        price=50,
        stock=0,
        category_id=category.id
    )

    db.add(product)
    db.commit()
    db.refresh(product)

    response = client.post(
        "/cart",
        json={
            "product_id": product.id,
            "quantity": 1
        },
        headers=headers
    )

    assert response.status_code == 400
    assert response.json()["detail"] == (
        "quantity solicitada maior que o stock disponível."
    )
    
def test_nao_adicionar_product_duplicado(db):

    client.post(
        "/users",
        json={
            "name": "Pedro",
            "email": "pedro@teste.com",
            "password": "Pedro123@"
        }
    )

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

    category = category(
        name="Canecas"
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

    # Primeira vez: deve funcionar
    response = client.post(
        "/cart",
        json={
            "product_id": product.id,
            "quantity": 2
        },
        headers=headers
    )

    assert response.status_code == 200

    # Segunda vez: não deve create outro item
    response = client.post(
        "/cart",
        json={
            "product_id": product.id,
            "quantity": 1
        },
        headers=headers
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "product já está no cart."

def test_get_cart(db):

    client.post(
        "/users",
        json={
            "name": "Pedro",
            "email": "pedro@teste.com",
            "password": "Pedro123@"
        }
    )

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

    category = category(
        name="Canecas"
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
        headers=headers
    )

    assert response.status_code == 200

    response = client.get(
        "/cart",
        headers=headers
    )

    assert response.status_code == 200

    dados = response.json()

    assert len(dados["items"]) == 1

    item = dados["items"][0]

    assert item["product_id"] == product.id
    assert item["name"] == "Caneca Naruto"
    assert item["preco"] == "50.00"
    assert item["quantity"] == 2
    assert item["subtotal"] == "100.00"

    assert dados["total"] == "100.00"
    
def test_alterar_quantity(db):

    client.post(
        "/users",
        json={
            "name": "Pedro",
            "email": "pedro@teste.com",
            "password": "Pedro123@"
        }
    )

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

    category = category(name="Canecas")

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
        headers=headers
    )

    assert response.status_code == 200

    response = client.patch(
        f"/cart/{product.id}",
        params={
            "quantity": 5
        },
        headers=headers
    )

    assert response.status_code == 200

    dados = response.json()

    assert dados["product_id"] == product.id
    assert dados["quantity"] == 5

def test_alterar_quantity_zero(db):

    client.post(
        "/users",
        json={
            "name": "Pedro",
            "email": "pedro@teste.com",
            "password": "Pedro123@"
        }
    )

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

    category = category(name="Canecas")

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

    client.post(
        "/cart",
        json={
            "product_id": product.id,
            "quantity": 2
        },
        headers=headers
    )

    response = client.patch(
        f"/cart/{product.id}",
        params={
            "quantity": 0
        },
        headers=headers
    )

    assert response.status_code == 400
    assert response.json()["detail"] == (
        "A quantity deve ser maior que zero."
    )

def test_alterar_quantity_maior_que_stock(db):

    client.post(
        "/users",
        json={
            "name": "Pedro",
            "email": "pedro@teste.com",
            "password": "Pedro123@"
        }
    )

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

    category = category(name="Canecas")

    db.add(category)
    db.commit()
    db.refresh(category)

    product = product(
        name="Caneca Naruto",
        price=50,
        stock=5,
        category_id=category.id
    )

    db.add(product)
    db.commit()
    db.refresh(product)

    client.post(
        "/cart",
        json={
            "product_id": product.id,
            "quantity": 2
        },
        headers=headers
    )

    response = client.patch(
        f"/cart/{product.id}",
        params={
            "quantity": 6
        },
        headers=headers
    )

    assert response.status_code == 400
    assert response.json()["detail"] == (
        "quantity solicitada maior que o stock disponível."
    )
    
def test_alterar_product_que_nao_esta_no_cart(db):

    client.post(
        "/users",
        json={
            "name": "Pedro",
            "email": "pedro@teste.com",
            "password": "Pedro123@"
        }
    )

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

    # Cria o cart vazio
    client.get(
        "/cart",
        headers=headers
    )

    category = category(name="Canecas")

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

    response = client.patch(
        f"/cart/{product.id}",
        params={
            "quantity": 5
        },
        headers=headers
    )

    assert response.status_code == 404
    assert response.json()["detail"] == (
        "product não está no cart."
    )
    
def test_remover_product_cart(db):

    client.post(
        "/users",
        json={
            "name": "Pedro",
            "email": "pedro@teste.com",
            "password": "Pedro123@"
        }
    )

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

    category = category(name="Canecas")

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
        headers=headers
    )

    assert response.status_code == 200

    # Remove
    response = client.delete(
        f"/cart/{product.id}",
        headers=headers
    )

    assert response.status_code == 200
    assert response.json()["message"] == (
        "product removido do cart."
    )

    response = client.get(
        "/cart",
        headers=headers
    )

    assert response.status_code == 200
    assert response.json()["items"] == []
    assert response.json()["total"] == "0"
    
def test_remover_product_que_nao_esta_no_cart(db):

    client.post(
        "/users",
        json={
            "name": "Pedro",
            "email": "pedro@teste.com",
            "password": "Pedro123@"
        }
    )
    
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
    
    client.get(
        "/cart",
        headers=headers
    )

    category = category(name="Canecas")

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

    response = client.delete(
        f"/cart/{product.id}",
        headers=headers
    )

    assert response.status_code == 404
    assert response.json()["detail"] == (
        "product não está no cart."
    )
    
def test_get_cart_vazio():

    client.post(
        "/users",
        json={
            "name": "Pedro",
            "email": "pedro@teste.com",
            "password": "Pedro123@"
        }
    )

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
        "/cart",
        headers=headers
    )

    assert response.status_code == 200

    dados = response.json()

    assert dados["items"] == []
    assert dados["total"] == "0"