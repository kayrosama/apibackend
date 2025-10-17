import pytest
from fastapi.testclient import TestClient
from jose import jwt
from datetime import datetime, timedelta, UTC
from main import app
from services.config import SECRET_KEY, ALGORITHM

client = TestClient(app)

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

TOKENS = {
    "sysoper_active": create_token("sys@example.com", "sysoper", True)
}

ENDPOINT = "/auth/register"

def test_sysoper_cannot_access():
    response = client.post(ENDPOINT, headers={"Authorization": TOKENS["sysoper_active"]}, json={
        "username": "sysuser",
        "password": "syspass",
        "email": "sysuser@example.com"
    })
    assert response.status_code == 403
