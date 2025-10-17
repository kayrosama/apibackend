import pytest

def test_register_success(test_client, admsys_token):
    response = test_client.post("/auth/register", headers={
        "Authorization": admsys_token
    }, json={
        "username": "newuser",
        "password": "securepass",
        "email": "newuser@example.com"
    })
    print("Step 01 :: test_register_success \n%s\n" % response.json())
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "newuser@example.com"
    assert data["username"] == "newuser"
    assert data["is_active"] is True
