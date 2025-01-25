from fastapi.testclient import TestClient
from app_fastapi.main import app

client = TestClient(app)

def test_create_user():
    response = client.post(
        "/users/",
        json={"username": "testuser", "email": "test@example.com", "password": "strongpassword"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"