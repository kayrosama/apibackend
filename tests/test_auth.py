from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_register_success():
    response = client.post("/auth/register", json={
        "username": "newuser",
        "password": "securepass",
        "email": "newuser@example.com"
    })
    assert response.status_code == 200
    assert "message" in response.json()

def test_register_duplicate_user():
    client.post("/auth/register", json={
        "username": "duplicateuser",
        "password": "securepass",
        "email": "duplicate@example.com"
    })
    response = client.post("/auth/register", json={
        "username": "duplicateuser",
        "password": "anotherpass",
        "email": "duplicate2@example.com"
    })
    assert response.status_code == 400
    assert response.json()["detail"] == "Username already exists"

def test_login_success():
    client.post("/auth/register", json={
        "username": "loginuser",
        "password": "mypassword",
        "email": "loginuser@example.com"
    })
    response = client.post("/auth/login", json={
        "username": "loginuser",
        "password": "mypassword"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_failure():
    response = client.post("/auth/login", json={
        "username": "nonexistent",
        "password": "wrongpass"
    })
    assert response.status_code == 401
    