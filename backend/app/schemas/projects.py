
from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel


class ProjectBase(SQLModel):
    title: str
    description: Optional[str] = None

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(ProjectBase):
    title: Optional[str] = None
    description: Optional[str] = None

class ProjectRead(ProjectBase):
    id: int
    created_at: datetime
    created_by_id: int