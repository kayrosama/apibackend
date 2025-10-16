import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
import sys
import os

# Ensure the current directory is in sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main import app
from services.database import Base, get_db

# Configuración de base de datos SQLite en memoria
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Crear tablas antes de ejecutar pruebas
Base.metadata.create_all(bind=engine)

# Override de la dependencia get_db para usar la base de datos de pruebas
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# Fixture para el cliente de pruebas
@pytest.fixture(scope="module")
def test_client():
    with TestClient(app) as client:
        yield client
