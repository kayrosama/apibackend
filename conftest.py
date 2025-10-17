import pytest
import os 
import sys
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from jose import jwt
from datetime import datetime, timedelta, UTC

# Ensure the current directory is in sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main import app
#from models import Base  # Asegúrate de importar Base desde donde defines tus modelos
from services.database import Base, get_db  # O el path correcto a tu función de dependencia

SECRET_KEY="Kawabonga69"
ALGORITHM="HS256"

# Usar SQLite en memoria para pruebas
SQLALCHEMY_DATABASE_URL = "sqlite:///./static/bdd/testing.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Crear las tablas antes de cada test
@pytest.fixture(scope="session", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

# Override de la dependencia de DB
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="function")
def db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        
# Cliente de prueba
@pytest.fixture()
def test_client():
    return TestClient(app)

# Fixture for admsys token
@pytest.fixture()
def admsys_token():
    expire = datetime.now(UTC) + timedelta(minutes=30)
    payload = {
        "sub": "admin@example.com",
        "role": "admsys",
        "is_active": True,
        "exp": expire
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return f"Bearer {token}"
    
@pytest.fixture
def create_admin_user():
    def _create(is_active=True):
        db = TestingSessionLocal()
        admin_user = User(
            username="admin",
            email="admin@example.com",
            password=get_password_hash("adminpass"),
            role="admsys",
            is_active=is_active
        )
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)
        db.close()
    return _create
    