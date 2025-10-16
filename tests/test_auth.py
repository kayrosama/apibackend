import pytest

# Usar el fixture test_client definido en conftest.py
def test_register_success(test_client):
    response = test_client.post("/auth/register", json={
        "username": "newuser",
        "password": "securepass",
        "email": "newuser@example.com"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "newuser@example.com"
    assert data["username"] == "newuser"
    assert data["is_active"] is True

def test_register_duplicate_user(test_client):
    test_client.post("/auth/register", json={
        "username": "duplicateuser",
        "password": "securepass",
        "email": "duplicate@example.com"
    })
    response = test_client.post("/auth/register", json={
        "username": "duplicateuser",
        "password": "anotherpass",
        "email": "duplicate@example.com"
    })
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"

def test_login_success(test_client):
    test_client.post("/auth/register", json={
        "username": "loginuser",
        "password": "mypassword",
        "email": "loginuser@example.com"
    })
    response = test_client.post("/auth/login", json={
        "email": "loginuser@example.com",
        "password": "mypassword"
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_failure(test_client):
    response = test_client.post("/auth/login", json={
        "email": "nonexistent@example.com",
        "password": "wrongpass"
    })
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid email or password"
    