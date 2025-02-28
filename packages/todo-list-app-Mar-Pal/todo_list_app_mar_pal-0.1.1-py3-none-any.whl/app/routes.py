from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.services import get_tasks, create_task, delete_task, update_task_status, update_task
from app.schemas import TaskCreate, TaskResponse
from app.auth import authenticate


router = APIRouter()

def get_db():

    db= SessionLocal()
    try: 
        yield db
    finally: 
        db.close()

@router.get("/tasks", response_model=list[TaskResponse])
def read_tasks(db: Session = Depends(get_db), user: str = Depends(authenticate)):
    return get_tasks(db)

@router.post("/tasks", response_model=TaskResponse)
def add_task(task: TaskCreate, db: Session = Depends(get_db), user: str = Depends(authenticate)):
    return create_task(db, task)

@router.delete("/tasks/{task_id}", response_model=TaskResponse)
def remove_task(task_id: int, db: Session = Depends(get_db), user: str = Depends(authenticate)):
    task = delete_task(db, task_id)
    if task:
        return task
    raise HTTPException(status_code=404, detail="Task not found")

@router.put("/tasks/{task_id}/complete", response_model=TaskResponse)
def complete_task(task_id: int, db: Session = Depends(get_db)):
    task = update_task_status(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.put("/tasks/{task_id}/edit", response_model=TaskResponse)
def edit_task(task_id: int, task_data: TaskCreate, db: Session = Depends(get_db)):
    task = update_task(db, task_id, task_data.title, task_data.description)

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

