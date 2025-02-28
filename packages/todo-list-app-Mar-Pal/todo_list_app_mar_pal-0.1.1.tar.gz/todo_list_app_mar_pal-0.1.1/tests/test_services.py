import pytest
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.services import create_task

@pytest.fixture
def db():
    db = SessionLocal()
    yield db
    db.close()

def test_create_task(db: Session):
    task = create_task(db, "New Task", "New Description")
    assert task.title == "New Task"
    assert task.description == "New Description"
    assert task.completed is False