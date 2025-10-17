import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
from jose import jwt
import logging

from main import app
from models.user import User, UserRole
from conftest import TestingSessionLocal
from utils.security import get_password_hash
from utils.logger import get_logger

logger = get_logger(__name__)

client = TestClient(app)

ENDPOINT = "/auth/register"
SECRET_KEY = "Kawabonga69"
ALGORITHM = "HS256"

def create_active_admsys_user(db: Session):
    logger.info("Creando usuario activo con rol admsys en la base de datos de pruebas.")
    user = User(
        username="adminactive",
        email="adminactive@example.com",
        password=get_password_hash("adminpass"),
        role=UserRole.admsys,
        is_active=False
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    logger.info(f"Usuario creado: {user.email}, activo: {user.is_active}, rol: {user.role}")
    return user

def generate_token(email: str, role: str):
    logger.info(f"Generando token JWT para el usuario {email} con rol {role}")
    expire = datetime.now(timezone.utc) + timedelta(minutes=30)
    payload = {
        "sub": email,
        "role": role,
        "exp": expire
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    logger.info(f"Token generado: {token}")
    return f"Bearer {token}"

def test_admsys_active_can_register_user():
    logger.info("Iniciando test: test_admsys_active_can_register_user")

    # Crear usuario activo
    db = TestingSessionLocal()
    admin_user = create_active_admsys_user(db)

    # Generar token
    token = generate_token(admin_user.email, admin_user.role)

    # Intentar registrar un nuevo usuario
    logger.info(f"Intentando registrar usuario con token de admsys activo.")
    response = client.post(
        ENDPOINT,
        headers={"Authorization": token},
        json={
            "username": "newuser",
            "password": "newpass",
            "email": "newuser@example.com",
            "first_name": "New",
            "last_name": "User",
            "role": "opera"
        }
    )

    logger.info(f"Respuesta recibida: status_code={response.status_code}, body={response.json()}")
    assert response.status_code == 200
    assert response.json()["email"] == "newuser@example.com"
    assert response.json()["role"] == "opera"
    logger.info("Test finalizado correctamente: usuario registrado por admsys activo.")

