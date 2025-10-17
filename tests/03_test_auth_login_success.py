import pytest
from jose import jwt
from datetime import datetime, timedelta
from services.config import SECRET_KEY, ALGORITHM

def test_login_success(test_client):
    expire = datetime.utcnow() + timedelta(minutes=30)
    payload = {
        "sub": "loginuser@example.com",
        "role": "admsys",
        "is_active": True,
        "exp": expire
    }
    admsys_token = f"Bearer {jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)}"

    test_client.post("/auth/register", headers={
        "Authorization": admsys_token
    }, json={
        "username": "loginuser",
        "password": "mypassword",
        "email": "loginuser@example.com"
    })
    response = test_client.post("/auth/login", json={
        "email": "loginuser@example.com",
        "password": "mypassword"
    })
    print("Step 03 :: test_login_success \n%s\n" % response.json())
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
