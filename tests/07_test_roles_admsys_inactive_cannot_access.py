import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
from jose import jwt

from main import app
from models.user import User, UserRole
from utils.security import get_password_hash
from services.database import get_db

client = TestClient(app)

ENDPOINT = "/auth/register"
SECRET_KEY = "Kawabonga69"
ALGORITHM = "HS256"

def create_inactive_admsys_user(db: Session):
    user = User(
        username="admin",
        email="admin@example.com",
        password=get_password_hash("adminpass"),
        role=UserRole.admsys,
        is_active=False  # Usuario inactivo
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def generate_token(email: str, role: str):
    expire = datetime.now(timezone.utc) + timedelta(minutes=30)
    payload = {
        "sub": email,
        "role": role,
        "exp": expire
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return f"Bearer {token}"

def test_admsys_inactive_cannot_access():
    # Crear usuario inactivo en la base de datos
    db = next(get_db())
    admin_user = create_inactive_admsys_user(db)

    # Generar token para el usuario inactivo
    token = generate_token(admin_user.email, admin_user.role)

    # Intentar registrar un nuevo usuario usando el token del usuario inactivo
    response = client.post(
        ENDPOINT,
        headers={"Authorization": token},
        json={
            "username": "inactiveadmin",
            "password": "adminpass",
            "email": "inactiveadmin@example.com",
            "first_name": "Inactive",
            "last_name": "Admin",
            "role": "opera"
        }
    )

    print("Step 07 :: test_admsys_inactive_cannot_access \n", response.json())
    assert response.status_code == 403
    