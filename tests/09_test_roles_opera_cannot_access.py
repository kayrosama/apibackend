import pytest
from fastapi.testclient import TestClient
from jose import jwt
from datetime import datetime, timedelta, UTC

from main import app
from conftest import TestingSessionLocal
from models.user import User
from utils.security import get_password_hash
client = TestClient(app)
SECRET_KEY = "Kawabonga69"
ALGORITHM = "HS256"
ENDPOINT = "/auth/register"

def create_opera_user():
    db = TestingSessionLocal()
    user = User(
        username="opera",
        email="op@example.com",
        password=get_password_hash("oppass"),
        role="opera",
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

def test_opera_cannot_access():
    # Crear usuario opera activo en la base de datos
    create_opera_user()

    # Generar token para el usuario opera
    token = create_token("op@example.com", "opera", True)

    # Intentar registrar un nuevo usuario usando el token del usuario opera
    response = client.post(ENDPOINT, headers={"Authorization": token}, json={
        "username": "opuser",
        "password": "oppass",
        "email": "opuser@example.com"
    })

    print("Step 09 :: test_opera_cannot_access \n", response.json())
    assert response.status_code == 403
    