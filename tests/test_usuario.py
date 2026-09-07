from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


def test_create_user():
    response = client.post(
        "/users",
        json={
            "name": "Pedro Hall",
            "email": "pedro@teste.com",
            "password": "Pedro123@"
        }
    )

    print(response.json())

    assert response.status_code == 200


def test_create_user_invalid_email():
    response = client.post(
        "/users",
        json={
            "name": "Pedro Hall",
            "email": "pedro_teste.com",
            "password": "Pedro123@"
        }
    )

    assert response.status_code == 422


def test_create_user_invalid_password():
    response = client.post(
        "/users",
        json={
            "name": "Pedro Hall",
            "email": "pedro@teste.com",
            "password": "pedro123"
        }
    )

    assert response.status_code == 422


def test_create_duplicate_user(db):
    response = client.post(
        "/users",
        json={
            "name": "Pedro Hall",
            "email": "pedro@teste.com",
            "password": "Pedro123@"
        }
    )

    assert response.status_code == 200

    response = client.post(
        "/users",
        json={
            "name": "Pedro Hall",
            "email": "pedro@teste.com",
            "password": "Pedro123@"
        }
    )

    print(response.json())

    assert response.status_code == 400


def test_login():
    client.post(
        "/users",
        json={
            "name": "Pedro Hall",
            "email": "pedro@teste.com",
            "password": "Pedro123@"
        }
    )

    response = client.post(
        "/users/login",
        json={
            "email": "pedro@teste.com",
            "password": "Pedro123@"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_invalid_password():
    client.post(
        "/users",
        json={
            "name": "Pedro Hall",
            "email": "pedro@teste.com",
            "password": "Pedro123@"
        }
    )

    response = client.post(
        "/users/login",
        json={
            "email": "pedro@teste.com",
            "password": "pedro123"
        }
    )

    assert response.status_code == 401


def test_get_current_user():
    client.post(
        "/users",
        json={
            "name": "Pedro Hall",
            "email": "pedro@teste.com",
            "password": "Pedro123@"
        }
    )

    response = client.post(
        "/users/login",
        json={
            "email": "pedro@teste.com",
            "password": "Pedro123@"
        }
    )

    data = response.json()
    token = data["access_token"]

    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = client.get(
        "/users/me",
        headers=headers
    )

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == "Pedro Hall"
    assert data["email"] == "pedro@teste.com"


def test_update_user_email():
    response = client.post(
        "/users",
        json={
            "name": "Pedro",
            "email": "pedro@email.com",
            "password": "Pedro123@"
        }
    )

    user_data = response.json()

    login = client.post(
        "/users/login",
        json={
            "email": "pedro@email.com",
            "password": "Pedro123@"
        }
    )

    token = login.json()["access_token"]

    response = client.patch(
        f"/users/{user_data['id']}",
        json={
            "email": "pedronovo@email.com"
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200
    assert response.json()["email"] == "pedronovo@email.com"


def test_update_user_password():
    response = client.post(
        "/users",
        json={
            "name": "Pedro",
            "email": "pedro@email.com",
            "password": "Pedro123@"
        }
    )

    user_data = response.json()

    login = client.post(
        "/users/login",
        json={
            "email": "pedro@email.com",
            "password": "Pedro123@"
        }
    )

    token = login.json()["access_token"]

    response = client.patch(
        f"/users/{user_data['id']}",
        json={
            "password": "Pedro123!"
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200

    new_login = client.post(
        "/users/login",
        json={
            "email": "pedro@email.com",
            "password": "Pedro123!"
        }
    )

    assert new_login.status_code == 200


def test_delete_user():
    response = client.post(
        "/users",
        json={
            "name": "Pedro",
            "email": "pedro@email.com",
            "password": "Pedro123@"
        }
    )

    user_data = response.json()

    login = client.post(
        "/users/login",
        json={
            "email": "pedro@email.com",
            "password": "Pedro123@"
        }
    )

    token = login.json()["access_token"]

    response = client.delete(
        f"/users/{user_data['id']}",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200

    login_after_delete = client.post(
        "/users/login",
        json={
            "email": "pedro@email.com",
            "password": "Pedro123@"
        }
    )

    assert login_after_delete.status_code == 401