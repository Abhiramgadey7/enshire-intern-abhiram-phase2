from app.auth import create_access_token


def test_register(client):
    response = client.post(
        "/register",
        json={
            "email": "user@test.com",
            "password": "password123",
            "role": "user"
        }
    )

    assert response.status_code == 201
    assert response.json()["email"] == "user@test.com"


def test_login(client):
    client.post(
        "/register",
        json={
            "email": "user@test.com",
            "password": "password123",
            "role": "user"
        }
    )

    response = client.post(
        "/login",
        data={
            "username": "user@test.com",
            "password": "password123"
        }
    )

    assert response.status_code == 200
    assert "access_token" in response.json()


def test_me(client):
    client.post(
        "/register",
        json={
            "email": "user@test.com",
            "password": "password123",
            "role": "user"
        }
    )

    token = client.post(
        "/login",
        data={
            "username": "user@test.com",
            "password": "password123"
        }
    ).json()["access_token"]

    response = client.get(
        "/me",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert response.json()["email"] == "user@test.com"


def test_admin_route(client):
    client.post(
        "/register",
        json={
            "email": "admin@test.com",
            "password": "password123",
            "role": "admin"
        }
    )

    token = client.post(
        "/login",
        data={
            "username": "admin@test.com",
            "password": "password123"
        }
    ).json()["access_token"]

    response = client.post(
        "/admin-only-route",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200