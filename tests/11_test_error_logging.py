import os
import json
import pytest
from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient
from pydantic import BaseModel
from middleware.error_handler import (
    log_exceptions_middleware,
    http_exception_handler,
    validation_exception_handler
)

app = FastAPI()
app.middleware("http")(log_exceptions_middleware)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(Exception, validation_exception_handler)

@app.get("/raise-http-exception")
def raise_http_exception():
    raise HTTPException(status_code=404, detail="Resource not found")

@app.get("/raise-exception")
def raise_exception():
    raise ValueError("Unexpected error occurred")

class Item(BaseModel):
    name: str
    quantity: int

@app.post("/validate-item")
def validate_item(item: Item):
    return item

client = TestClient(app)

def test_http_exception_logging():
    response = client.get("/raise-http-exception")
    assert response.status_code == 404
    assert response.json()["detail"] == "Resource not found"

def test_generic_exception_logging():
    response = client.get("/raise-exception")
    assert response.status_code == 500
    assert response.json()["detail"] == "Internal Server Error"

def test_validation_error_logging():
    response = client.post("/validate-item", json={"name": "Widget", "quantity": "invalid"})
    assert response.status_code == 422
    assert "detail" in response.json()

def test_log_file_created_and_contains_entries():
    log_file = "var_logs/SystemOut.log"
    assert os.path.exists(log_file)
    with open(log_file, "r") as f:
        logs = f.readlines()
        messages = [json.loads(log)["message"] for log in logs]
        assert any("Resource not found" in msg for msg in messages)
        assert any("Unexpected error occurred" in msg for msg in messages)
        assert any("Validation error" in msg for msg in messages)

def test_log_file_created_and_contains_entries():
    log_file = "var_logs/SystemOut.log"
    assert os.path.exists(log_file)
    with open(log_file, "r") as f:
        logs = f.readlines()
        messages = [json.loads(log)["message"] for log in logs]

        assert any("Resource not found" in msg for msg in messages)
        assert any("Unexpected error occurred" in msg for msg in messages)

        # Validación condicional para errores de validación
        if not any(
            "Validation error" in msg or
            "value is not a valid integer" in msg or
            "validation error" in msg.lower()
            for msg in messages
            ):
            pytest.fail("Validation error message not found in logs. Anomaly detected.")
