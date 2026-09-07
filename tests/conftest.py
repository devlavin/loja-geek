from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import pytest

from main import app
from database import get_db
from models import Base, User, Category, Product
from auth import create_token


DATABASE_URL_TEST = (
    "postgresql+psycopg://postgres:minha_senha@localhost:5433/fastapi_produtos_test"
)

engine_test = create_engine(DATABASE_URL_TEST)

TestingSessionLocal = sessionmaker(
    bind=engine_test,
    autocommit=False,
    autoflush=False
)


def override_get_db():
    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True)
def clear_database():
    Base.metadata.drop_all(bind=engine_test)
    Base.metadata.create_all(bind=engine_test)

    yield


@pytest.fixture
def db():
    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def user(db):
    user = User(
        name="Pedro",
        email="pedro@teste.com",
        password_hash="Pedro123@",
        role="user"
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


@pytest.fixture
def admin(db):
    admin = User(
        name="Admin Teste",
        email="admin@test.com",
        password_hash="password_hash_teste",
        role="admin"
    )

    db.add(admin)
    db.commit()
    db.refresh(admin)

    return admin


@pytest.fixture
def user_token(user):
    return create_token(user.id)


@pytest.fixture
def admin_token(admin):
    return create_token(admin.id)


@pytest.fixture
def user_headers(user_token):
    return {
        "Authorization": f"Bearer {user_token}"
    }


@pytest.fixture
def admin_headers(admin_token):
    return {
        "Authorization": f"Bearer {admin_token}"
    }


@pytest.fixture
def category(db):
    category = Category(name="Geek")

    db.add(category)
    db.commit()
    db.refresh(category)

    return category


@pytest.fixture
def product(db, category):
    product = Product(
        name="Caneca Naruto",
        price=50,
        stock=10,
        category_id=category.id
    )

    db.add(product)
    db.commit()
    db.refresh(product)

    return product