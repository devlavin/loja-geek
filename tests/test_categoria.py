from fastapi.testclient import TestClient

from main import app
from models import Category, Product

client = TestClient(app)


def test_list_categories():
    response = client.get("/categories")

    assert response.status_code == 200


def test_create_category_in_database(admin_headers):
    response = client.post(
        "/categories",
        json={
            "name": "Jogos"
        },
        headers=admin_headers
    )

    assert response.status_code == 200


def test_get_category(admin_headers, db, category):
    response = client.get(
        f"/categories/{category.id}",
        headers=admin_headers
    )

    assert response.status_code == 200


def test_update_category(admin_headers, db, category):
    response = client.patch(
        f"/categories/{category.id}",
        json={
            "name": "Chaveirinhos"
        },
        headers=admin_headers
    )

    assert response.status_code == 200


def test_delete_category(admin_headers, db, category):
    category_id = category.id

    response = client.delete(
        f"/categories/{category_id}",
        headers=admin_headers
    )

    assert response.status_code == 200

    deleted_category = db.query(Category).filter(
        Category.id == category_id
    ).first()

    assert deleted_category is None


def test_cannot_delete_category_with_products(
    admin_headers,
    db,
    category
):
    product = Product(
        name="Chinelo Sonserina",
        price=99.99,
        stock=25,
        category_id=category.id
    )

    db.add(product)
    db.commit()
    db.refresh(product)

    category_id = category.id

    response = client.delete(
        f"/categories/{category_id}",
        headers=admin_headers
    )

    assert response.status_code == 400

    category_in_database = db.query(Category).filter(
        Category.id == category_id
    ).first()

    assert category_in_database is not None