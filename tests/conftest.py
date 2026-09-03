from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app
from database import get_db

from models import Base, Usuario, Produto
from auth import criar_token
from fastapi import Query

DATABASE_URL_TEST = "postgresql+psycopg://postgres:kryptonianke@localhost:5432/fastapi_produtos_test"

engine_test = create_engine(DATABASE_URL_TEST)

TestingSessionLocal = sessionmaker(
    bind=engine_test,
    autocommit=False,
    autoflush=False
)

Base.metadata.create_all(bind=engine_test)

def override_get_db():
    db = TestingSessionLocal()
    
    try:
        yield db
    finally:
        db.close()
        
app.dependency_overrides[get_db] = override_get_db

import pytest

@pytest.fixture
def db():
    db = TestingSessionLocal()
    
    try:
        yield db
    finally:
        db.close()

@pytest.fixture
def admin_token(db):
    admin = Usuario(
        name="Admin Teste",
        email="admin@test.com",
        password_hash="senha_hash_teste",
        role="admin"
    )

    db.add(admin)
    db.commit()
    db.refresh(admin)

    token = criar_token(admin.id)

    return token

@pytest.fixture(autouse=True)
def limpar_banco(db):
    Base.metadata.drop_all(bind=engine_test)
    Base.metadata.create_all(bind=engine_test)
    
    yield

            


