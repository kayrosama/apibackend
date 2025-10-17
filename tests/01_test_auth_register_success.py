import pytest
from conftest import TestingSessionLocal
from models.user import User
from utils.security import get_password_hash

def test_register_success(test_client, admsys_token):
    # Crear usuario admin en la base de datos
    db = TestingSessionLocal()
    admin_user = User(
        username="admin",
        email="admin@example.com",
        password=get_password_hash("adminpass"),  # ✅ corregido
        role="admsys",
        is_active=True
    )
    db.add(admin_user)
    db.commit()
    db.refresh(admin_user)
    db.close()

    # Probar el registro protegido
    response = test_client.post("/auth/register", headers={
        "Authorization": admsys_token
    }, json={
        "username": "newuser",
        "password": "securepass",
        "email": "newuser@example.com"
    })

    print("Step 01 :: test_register_success \n%s\n" % response.json())
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "newuser@example.com"
    assert data["username"] == "newuser"
    assert data["is_active"] is True
    