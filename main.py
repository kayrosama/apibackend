from fastapi import FastAPI
from contextlib import asynccontextmanager
from routers import auth  # , tasks
from services.database import Base, engine

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Crear tablas en la base de datos (útil para SQLite en pruebas)
    Base.metadata.create_all(bind=engine)
    yield
    # Aquí podrías agregar lógica de limpieza si fuera necesario

app = FastAPI(title="API Backend", lifespan=lifespan)

# Registrar routers
app.include_router(auth.router, prefix="/auth", tags=["auth"])
