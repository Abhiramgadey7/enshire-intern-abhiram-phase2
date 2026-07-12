from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_invalid_student_id():

    response = client.get("/students/999999")

    assert response.status_code in [401, 404]


def test_home():

    response = client.get("/")

    assert response.status_code == 200

    assert "Student Management API Running" in response.text