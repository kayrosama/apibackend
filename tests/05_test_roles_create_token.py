import pytest
from jose import jwt
from datetime import datetime, timedelta, UTC

# Configuración de seguridad
SECRET_KEY = "Kawabonga69"
ALGORITHM = "HS256"

# Función para crear tokens
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

# Pruebas automatizadas para validar tokens
@pytest.mark.parametrize("email,role,is_active", [
    ("admin@example.com", "admsys", True),
    ("admin@example.com", "admsys", False),
    ("sys@example.com", "sysoper", True),
    ("op@example.com", "opera", True),
])
def test_token_structure_and_payload(email, role, is_active):
    token = create_token(email, role, is_active)
    assert token.startswith("Bearer ")
    encoded = token.split(" ")[1]
    decoded = jwt.decode(encoded, SECRET_KEY, algorithms=[ALGORITHM])
    assert decoded["sub"] == email
    assert decoded["role"] == role
    assert decoded["is_active"] == is_active
    assert "exp" in decoded
    