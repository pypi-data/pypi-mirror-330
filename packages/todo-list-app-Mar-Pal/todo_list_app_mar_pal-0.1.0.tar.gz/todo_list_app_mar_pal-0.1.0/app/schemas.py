from pydantic import BaseModel
from datetime import datetime

class TaskBase(BaseModel):

    title: str
    description: str | None = None
    completed: bool = False

class TaskCreate(TaskBase):
    pass

class TaskResponse(TaskBase):
    id: int
    title: str
    description: str | None
    completed: bool
    timestamp: datetime

    class Config: 
        from_attributes = True