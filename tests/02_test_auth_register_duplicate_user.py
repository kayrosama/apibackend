import pytest

def test_register_duplicate_user(test_client, admsys_token):
    test_client.post("/auth/register", headers={
        "Authorization": admsys_token
    }, json={
        "username": "duplicateuser",
        "password": "securepass",
        "email": "duplicate@example.com"
    })
    response = test_client.post("/auth/register", headers={
        "Authorization": admsys_token
    }, json={
        "username": "duplicateuser",
        "password": "anotherpass",
        "email": "duplicate@example.com"
    })
    print("Step 02 :: test_register_duplicate_user \n%s\n" % response.json())
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"
