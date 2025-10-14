from fastapi import APIRouter, HTTPException
from models.task import Task
from services.task_service import (
    create_task, get_tasks, get_task, update_task, delete_task
)

router = APIRouter()

@router.post("/")
def create(task: Task):
    return create_task(task)

@router.get("/")
def read_all():
    return get_tasks()

@router.get("/{task_id}")
def read(task_id: int):
    task = get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.put("/{task_id}")
def update(task_id: int, task: Task):
    return update_task(task_id, task)

@router.delete("/{task_id}")
def delete(task_id: int):
    return delete_task(task_id)
    
