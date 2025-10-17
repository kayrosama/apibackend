import pytest
from conftest import TestingSessionLocal
from models.user import User
from utils.security import get_password_hash

def test_register_duplicate_user(test_client, admsys_token):
    # Crear usuario admin en la base de datos
    db = TestingSessionLocal()
    admin_user = User(
        username="admin",
        email="admin@example.com",
        password=get_password_hash("adminpass"),
        role="admsys",
        is_active=True
    )
    db.add(admin_user)
    db.commit()
    db.refresh(admin_user)
    db.close()

    # Primer registro
    test_client.post("/auth/register", headers={
        "Authorization": admsys_token
    }, json={
        "username": "duplicateuser",
        "password": "securepass",
        "email": "duplicate@example.com"
    })

    # Intento duplicado
    response = test_client.post("/auth/register", headers={
        "Authorization": admsys_token
    }, json={
        "username": "duplicateuser",
        "password": "anotherpass",
        "email": "duplicate@example.com"
    })

    print("Step 02 :: test_register_duplicate_user \n%s\n" % response.json())
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"
    