import pytest

def test_login_failure(test_client):
    response = test_client.post("/auth/login", json={
        "email": "nonexistent@example.com",
        "password": "wrongpass"
    })
    print("Step 04 :: test_login_failure \n%s\n" % response.json())
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid email or password"
    