
from datetime import datetime, date
from enum import Enum
from typing import Optional

from sqlmodel import Field, SQLModel

class TaskPriority(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"

class TaskStatus(SQLModel, table=True):
    __tablename__ = "task_statuses"
    id: Optional[int] = Field(default=None, primary_key=True)
    key: str = Field(unique=True, index=True)
    name: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Task(SQLModel, table=True):
    __tablename__ = "tasks"
    id: Optional[int] = Field(default=None, primary_key=True)
    project_id: int = Field(foreign_key="projects.id")
    title: str
    description: Optional[str] = None
    status_id: int = Field(foreign_key="task_statuses.id")
    priority: TaskPriority = Field(default=TaskPriority.MEDIUM)
    due_date: Optional[date] = None
    created_by: int = Field(foreign_key="users.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)