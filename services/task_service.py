from models.task import Task

tasks_db = {}

def create_task(task: Task):
    tasks_db[task.id] = task
    return task

def get_tasks():
    return list(tasks_db.values())

def get_task(task_id: int):
    return tasks_db.get(task_id)

def update_task(task_id: int, task: Task):
    tasks_db[task_id] = task
    return task

def delete_task(task_id: int):
    return tasks_db.pop(task_id, None)
    
