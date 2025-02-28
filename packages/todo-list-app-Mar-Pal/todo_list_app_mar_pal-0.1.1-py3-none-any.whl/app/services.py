from sqlalchemy.orm import Session
from app.models import Task
from app.schemas import TaskCreate

def get_tasks(db: Session):

    return db.query(Task).all()

def create_task(db: Session, task: TaskCreate):

    new_task = Task(**task.model_dump())
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

def delete_task(db: Session, task_id: int):

    task = db.query(Task).filter(Task.id == task_id).first()
    if task: 
        db.delete(task)
        db.commit()
        return task
    return None

def update_task_status(db:Session, task_id: int):
    task = db.query(Task).filter(Task.id == task_id).first()
    if task: 
        task.completed = not task.completed
        db.commit()
        db.refresh(task)
        return task
    return None

def update_task(db: Session, task_id: int, title: str = None, description:str = None):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        return None
    if title is not None:
        task.title = title
    if description is not None:
        task.description = description
    
    db.commit()
    db.refresh(task)
    return task