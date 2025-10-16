from fastapi import FastAPI
from routers import auth #, tasks 
from services.database import Base, engine

app = FastAPI(title="API Backend")

#app.include_router(auth.router)
app.include_router(auth.router, prefix="/auth", tags=["auth"])
#app.include_router(tasks.router, prefix="/tasks", tags=["tasks"])

# Crear tablas en la base de datos (útil para SQLite en pruebas)
@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)
