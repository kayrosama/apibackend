from fastapi import FastAPI
from routers import auth, tasks

app = FastAPI()

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(tasks.router, prefix="/tasks", tags=["tasks"])
