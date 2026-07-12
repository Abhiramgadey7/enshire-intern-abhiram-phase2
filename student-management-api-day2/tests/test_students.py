def get_token(client):
    client.post(
        "/register",
        json={
            "email": "user@test.com",
            "password": "password123",
            "role": "user"
        }
    )

    return client.post(
        "/login",
        data={
            "username": "user@test.com",
            "password": "password123"
        }
    ).json()["access_token"]


def test_create_student(client):
    token = get_token(client)

    response = client.post(
        "/students",
        json={
            "name": "John",
            "age": 20,
            "course": "CSE"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200


def test_get_students(client):
    token = get_token(client)

    client.post(
        "/students",
        json={
            "name": "John",
            "age": 20,
            "course": "CSE"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    response = client.get(
        "/students",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200


def test_get_student(client):
    token = get_token(client)

    student = client.post(
        "/students",
        json={
            "name": "John",
            "age": 20,
            "course": "CSE"
        },
        headers={"Authorization": f"Bearer {token}"}
    ).json()

    response = client.get(
        f"/students/{student['id']}",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200


def test_update_student(client):
    token = get_token(client)

    student = client.post(
        "/students",
        json={
            "name": "John",
            "age": 20,
            "course": "CSE"
        },
        headers={"Authorization": f"Bearer {token}"}
    ).json()

    response = client.put(
        f"/students/{student['id']}",
        json={
            "name": "Ram",
            "age": 21,
            "course": "ECE"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200


def test_delete_student(client):
    token = get_token(client)

    student = client.post(
        "/students",
        json={
            "name": "John",
            "age": 20,
            "course": "CSE"
        },
        headers={"Authorization": f"Bearer {token}"}
    ).json()

    response = client.delete(
        f"/students/{student['id']}",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200