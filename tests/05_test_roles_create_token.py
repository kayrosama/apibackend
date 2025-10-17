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
    "admsys_active": create_token("admin@example.com", "admsys", True),
    "admsys_inactive": create_token("admin@example.com", "admsys", False),
    "sysoper_active": create_token("sys@example.com", "sysoper", True),
    "opera_active": create_token("op@example.com", "opera", True),
    "no_token": None
}

for key, token in TOKENS.items():
    if token:
        print(f"{key}: {token[:30]}...")  # Muestra solo los primeros 30 caracteres
    else:
        print(f"{key}: None")
