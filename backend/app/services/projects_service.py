
from typing import List, Optional
from fastapi import Depends
from sqlmodel import Session, select

from app.schemas.projects import ProjectCreate
from app.models.projects import Project
from app.db.session import get_session

class ProjectService:
    def __init__(self, session: Session):
        self.session = session
    
    def create_project(self, project_in: ProjectCreate, user_id: int) -> ProjectCreate:
        project = Project(
            **project_in.model_dump(),
            created_by_id=user_id
        )
        self.session.add(project)
        self.session.commit()
        self.session.refresh(project)
        return project
    
    def get_user_projects(self, user_id: int) -> List[Project]:
        statement = select(Project).where(Project.created_by_id == user_id)
        results = self.session.exec(statement)
        return results.all()
    
    def get_project_by_id(self, project_id: int) -> Optional[Project]:
        return self.session.get(Project, project_id)
    
def get_project_service(session: Session = Depends(get_session)) -> ProjectService:
    return ProjectService(session)