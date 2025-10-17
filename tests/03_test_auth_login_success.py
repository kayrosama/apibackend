import pytest
from conftest import TestingSessionLocal
from models.user import User
from utils.security import get_password_hash
from jose import jwt
from datetime import datetime, timedelta, UTC

SECRET_KEY="Kawabonga69"
ALGORITHM="HS256"

def test_login_success(test_client):
    # Crear usuario admin para validar el token
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

    # Generar token admsys
    expire = datetime.now(UTC) + timedelta(minutes=30)
    payload = {
        "sub": "admin@example.com",
        "role": "admsys",
        "is_active": True,
        "exp": expire
    }
    admsys_token = f"Bearer {jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)}"

    # Registrar usuario loginuser
    test_client.post("/auth/register", headers={
        "Authorization": admsys_token
    }, json={
        "username": "loginuser",
        "password": "mypassword",
        "email": "loginuser@example.com"
    })

    db.close()

    # Probar login
    response = test_client.post("/auth/login", json={
        "email": "loginuser@example.com",
        "password": "mypassword"
    })

    print("Step 03 :: test_login_success \n%s\n" % response.json())
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"