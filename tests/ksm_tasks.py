from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_task():
    response = client.post("/tasks/", json={"id": 1, "title": "Test Task", "description": "A task", "completed": False})
    assert response.status_code == 200

def test_get_task():
    client.post("/tasks/", json={"id": 2, "title": "Another Task", "description": "Another", "completed": False})
    response = client.get("/tasks/2")
    assert response.status_code == 200
    assert response.json()["title"] == "Another Task"
    
