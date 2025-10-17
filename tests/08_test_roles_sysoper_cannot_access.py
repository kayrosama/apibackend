import pytest
from fastapi.testclient import TestClient
from jose import jwt
from datetime import datetime, timedelta, UTC
from main import app
from services.database import get_db
from models.user import User
from utils.security import get_password_hash

client = TestClient(app)
ENDPOINT = "/auth/register"
SECRET_KEY = "Kawabonga69"
ALGORITHM = "HS256"

def create_sysoper_user():
    db = next(get_db())
    user = User(
        username="sysoper",
        email="sys@example.com",
        password=get_password_hash("syspass"),
        role="sysoper",
        is_active=True
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    db.close()

def create_token(email: str, role: str, is_active: bool = True):
    expire = datetime.now(UTC) + timedelta(minutes=30)
    payload = {
        "sub": email,
        "role": role,
        "is_active": is_active,
        "exp": expire
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return f"Bearer {token}"

def test_sysoper_cannot_access():
    # Crear usuario sysoper activo en la base de datos
    create_sysoper_user()

    # Generar token para el usuario sysoper
    token = create_token("sys@example.com", "sysoper", True)

    # Intentar registrar un nuevo usuario usando el token de sysoper
    response = client.post(ENDPOINT, headers={"Authorization": token}, json={
        "username": "sysuser",
        "password": "syspass",
        "email": "sysuser@example.com"
    })

    print("Step 08 :: test_sysoper_cannot_access \n", response.json())
    assert response.status_code == 403
    