from fastapi.testclient import TestClient

from main import app
from models import Product, Category


client = TestClient(app)


def test_list_products():
    response = client.get("/products")

    assert response.status_code == 200


def test_get_product(admin_token, db):
    category = Category(
        name="Chinelo"
    )

    db.add(category)
    db.commit()
    db.refresh(category)

    product = Product(
        name="Chinelo Grifinoria",
        price=99.99,
        stock=14,
        category_id=category.id
    )

    db.add(product)
    db.commit()
    db.refresh(product)

    headers = {
        "Authorization": f"Bearer {admin_token}"
    }

    response = client.get(
        f"/products/{product.id}",
        headers=headers
    )

    assert response.status_code == 200


def test_create_product_in_database(db):
    category = Category(
        name="Category Test"
    )

    db.add(category)
    db.commit()
    db.refresh(category)

    product = Product(
        name="Camiseta Teste",
        price=39.99,
        stock=10,
        category_id=category.id
    )

    db.add(product)
    db.commit()
    db.refresh(product)

    assert product.id is not None
    assert product.name == "Camiseta Teste"
    assert product.stock == 10
    assert product.category_id == category.id


def test_create_product(admin_token, db):
    category = Category(
        name="Harry Potter"
    )

    db.add(category)
    db.commit()
    db.refresh(category)

    headers = {
        "Authorization": f"Bearer {admin_token}"
    }

    response = client.post(
        "/products",
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


def test_update_product_price(admin_token, db):
    category = Category(
        name="Jogos Vorazes"
    )

    db.add(category)
    db.commit()
    db.refresh(category)

    product = Product(
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
        headers=headers
    )

    assert response.status_code == 200


def test_update_product_stock(admin_token, db):
    category = Category(
        name="Maze Runner"
    )

    db.add(category)
    db.commit()
    db.refresh(category)

    product = Product(
        name="Maze Runner: Correr ou Morrer",
        price=45.79,
        stock=12,
        category_id=category.id
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
        headers=headers
    )

    assert response.status_code == 200


def test_delete_product(admin_token, db):
    category = Category(
        name="Percy Jackson"
    )

    db.add(category)
    db.commit()
    db.refresh(category)

    product = Product(
        name="Camiseta Tridente Poseidon",
        price=57.99,
        stock=5,
        category_id=category.id
    )

    db.add(product)
    db.commit()
    db.refresh(product)

    product_id = product.id

    headers = {
        "Authorization": f"Bearer {admin_token}"
    }

    response = client.delete(
        f"/products/{product_id}",
        headers=headers
    )

    assert response.status_code == 200

    deleted_product = db.query(Product).filter(
        Product.id == product_id
    ).first()

    assert deleted_product is None
