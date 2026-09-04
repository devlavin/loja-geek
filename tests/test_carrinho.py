from fastapi.testclient import TestClient

from main import app
from models import Categoria, Produto

client = TestClient(app)

def test_adicionar_produto_carrinho(db):

    resposta = client.post(
        "/usuarios",
        json={
            "name": "Pedro",
            "email": "pedro@teste.com",
            "password": "Pedro123@"
        }
    )

    assert resposta.status_code == 200

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
        name="Canecas"
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
    
    resposta = client.post(
        "/carrinho",
        json={
            "produto_id": produto.id,
            "quantidade": 2
        },
        headers=headers
    )

    assert resposta.status_code == 200

    dados = resposta.json()

    assert len(dados["itens"]) == 1
    assert dados["itens"][0]["produto_id"] == produto.id
    assert dados["itens"][0]["quantidade"] == 2
    assert dados["itens"][0]["preco"] == "50.00"
    assert dados["itens"][0]["subtotal"] == "100.00"
    assert dados["total"] == "100.00"
    
def test_nao_adicionar_quantidade_maior_que_estoque(db):

    resposta = client.post(
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
        name="Canecas"
    )

    db.add(categoria)
    db.commit()
    db.refresh(categoria)

    produto = Produto(
        name="Caneca Naruto",
        price=50,
        estoque=5,
        category_id=categoria.id
    )

    db.add(produto)
    db.commit()
    db.refresh(produto)

    resposta = client.post(
        "/carrinho",
        json={
            "produto_id": produto.id,
            "quantidade": 6
        },
        headers=headers
    )

    assert resposta.status_code == 400
    assert resposta.json()["detail"] == (
        "Quantidade solicitada maior que o estoque disponível."
    )

def test_adicionar_produto_inexistente():

    resposta = client.post(
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

    resposta = client.post(
        "/carrinho",
        json={
            "produto_id": 9999,
            "quantidade": 1
        },
        headers=headers
    )

    assert resposta.status_code == 404
    assert resposta.json()["detail"] == "Produto não encontrado."
    
def test_adicionar_produto_sem_estoque(db):

    client.post(
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
        name="Canecas"
    )

    db.add(categoria)
    db.commit()
    db.refresh(categoria)

    produto = Produto(
        name="Caneca Naruto",
        price=50,
        estoque=0,
        category_id=categoria.id
    )

    db.add(produto)
    db.commit()
    db.refresh(produto)

    resposta = client.post(
        "/carrinho",
        json={
            "produto_id": produto.id,
            "quantidade": 1
        },
        headers=headers
    )

    assert resposta.status_code == 400
    assert resposta.json()["detail"] == (
        "Quantidade solicitada maior que o estoque disponível."
    )
    
def test_nao_adicionar_produto_duplicado(db):

    client.post(
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
        name="Canecas"
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

    # Primeira vez: deve funcionar
    resposta = client.post(
        "/carrinho",
        json={
            "produto_id": produto.id,
            "quantidade": 2
        },
        headers=headers
    )

    assert resposta.status_code == 200

    # Segunda vez: não deve criar outro item
    resposta = client.post(
        "/carrinho",
        json={
            "produto_id": produto.id,
            "quantidade": 1
        },
        headers=headers
    )

    assert resposta.status_code == 400
    assert resposta.json()["detail"] == "Produto já está no carrinho."

def test_visualizar_carrinho(db):

    client.post(
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
        name="Canecas"
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

    resposta = client.post(
        "/carrinho",
        json={
            "produto_id": produto.id,
            "quantidade": 2
        },
        headers=headers
    )

    assert resposta.status_code == 200

    resposta = client.get(
        "/carrinho",
        headers=headers
    )

    assert resposta.status_code == 200

    dados = resposta.json()

    assert len(dados["itens"]) == 1

    item = dados["itens"][0]

    assert item["produto_id"] == produto.id
    assert item["nome"] == "Caneca Naruto"
    assert item["preco"] == "50.00"
    assert item["quantidade"] == 2
    assert item["subtotal"] == "100.00"

    assert dados["total"] == "100.00"
    
def test_alterar_quantidade(db):

    client.post(
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

    categoria = Categoria(name="Canecas")

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

    resposta = client.post(
        "/carrinho",
        json={
            "produto_id": produto.id,
            "quantidade": 2
        },
        headers=headers
    )

    assert resposta.status_code == 200

    resposta = client.patch(
        f"/carrinho/{produto.id}",
        params={
            "quantidade": 5
        },
        headers=headers
    )

    assert resposta.status_code == 200

    dados = resposta.json()

    assert dados["produto_id"] == produto.id
    assert dados["quantidade"] == 5

def test_alterar_quantidade_zero(db):

    client.post(
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

    categoria = Categoria(name="Canecas")

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

    client.post(
        "/carrinho",
        json={
            "produto_id": produto.id,
            "quantidade": 2
        },
        headers=headers
    )

    resposta = client.patch(
        f"/carrinho/{produto.id}",
        params={
            "quantidade": 0
        },
        headers=headers
    )

    assert resposta.status_code == 400
    assert resposta.json()["detail"] == (
        "A quantidade deve ser maior que zero."
    )

def test_alterar_quantidade_maior_que_estoque(db):

    client.post(
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

    categoria = Categoria(name="Canecas")

    db.add(categoria)
    db.commit()
    db.refresh(categoria)

    produto = Produto(
        name="Caneca Naruto",
        price=50,
        estoque=5,
        category_id=categoria.id
    )

    db.add(produto)
    db.commit()
    db.refresh(produto)

    client.post(
        "/carrinho",
        json={
            "produto_id": produto.id,
            "quantidade": 2
        },
        headers=headers
    )

    resposta = client.patch(
        f"/carrinho/{produto.id}",
        params={
            "quantidade": 6
        },
        headers=headers
    )

    assert resposta.status_code == 400
    assert resposta.json()["detail"] == (
        "Quantidade solicitada maior que o estoque disponível."
    )
    
def test_alterar_produto_que_nao_esta_no_carrinho(db):

    client.post(
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

    # Cria o carrinho vazio
    client.get(
        "/carrinho",
        headers=headers
    )

    categoria = Categoria(name="Canecas")

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

    resposta = client.patch(
        f"/carrinho/{produto.id}",
        params={
            "quantidade": 5
        },
        headers=headers
    )

    assert resposta.status_code == 404
    assert resposta.json()["detail"] == (
        "Produto não está no carrinho."
    )
    
def test_remover_produto_carrinho(db):

    client.post(
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

    categoria = Categoria(name="Canecas")

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

    resposta = client.post(
        "/carrinho",
        json={
            "produto_id": produto.id,
            "quantidade": 2
        },
        headers=headers
    )

    assert resposta.status_code == 200

    # Remove
    resposta = client.delete(
        f"/carrinho/{produto.id}",
        headers=headers
    )

    assert resposta.status_code == 200
    assert resposta.json()["message"] == (
        "Produto removido do carrinho."
    )

    resposta = client.get(
        "/carrinho",
        headers=headers
    )

    assert resposta.status_code == 200
    assert resposta.json()["itens"] == []
    assert resposta.json()["total"] == "0"
    
def test_remover_produto_que_nao_esta_no_carrinho(db):

    client.post(
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
    
    client.get(
        "/carrinho",
        headers=headers
    )

    categoria = Categoria(name="Canecas")

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

    resposta = client.delete(
        f"/carrinho/{produto.id}",
        headers=headers
    )

    assert resposta.status_code == 404
    assert resposta.json()["detail"] == (
        "Produto não está no carrinho."
    )
    
def test_visualizar_carrinho_vazio():

    client.post(
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

    resposta = client.get(
        "/carrinho",
        headers=headers
    )

    assert resposta.status_code == 200

    dados = resposta.json()

    assert dados["itens"] == []
    assert dados["total"] == "0"