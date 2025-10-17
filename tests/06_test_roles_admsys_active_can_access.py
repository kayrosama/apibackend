import pytest
from conftest import TestingSessionLocal
from models.user import User
from utils.security import get_password_hash
from main import app
from fastapi.testclient import TestClient
from jose import jwt
from datetime import datetime, timedelta, UTC
from conftest import TestingSessionLocal 
    
client = TestClient(app)

SECRET_KEY = "Kawabonga69"
ALGORITHM = "HS256"
ENDPOINT = "/auth/register"

def test_admsys_active_can_access():
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

    # Probar acceso con token admsys activo
    expire = datetime.now(UTC) + timedelta(minutes=30)
    payload = {
        "sub": "admin@example.com",
        "role": "admsys",
        "is_active": True,
        "exp": expire
    }
    admsys_token = f"Bearer {jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)}"

    response = client.post(ENDPOINT, headers={"Authorization": admsys_token}, json={
        "username": "adminuser",
        "password": "adminpass",
        "email": "adminuser@example.com"
    })

    print("Step 06 :: test_admsys_active_can_access \n%s\n" % response.json())
    assert response.status_code == 200
