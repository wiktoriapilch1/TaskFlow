from datetime import date, datetime
from typing import List, Optional
from pydantic import BaseModel

from app.schemas.user import UserRead

from app.models.task import TaskPriority

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    priority: TaskPriority = TaskPriority.MEDIUM
    due_date: Optional[date] = None

class TaskCreate(TaskBase):
    project_id: int
    status_id: int
    assignee_ids: List[int] = []

class TaskRead(TaskBase):
    id: int
    project_id: int
    status_id: int
    created_by: int
    created_at: datetime
    assignees: List[UserRead] = []