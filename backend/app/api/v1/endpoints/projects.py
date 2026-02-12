from typing import List
from fastapi import APIRouter, Depends
from app.api.deps import CurrentUser
from app.schemas.projects import ProjectCreate, ProjectRead
from app.services.projects_service import ProjectService, get_project_service

router = APIRouter()

@router.post("/", response_model=ProjectRead, status_code=201)
def create_project(*, project_in: ProjectCreate, current_user: CurrentUser, service: ProjectService = Depends(get_project_service)):
    return service.create_project(project_in=project_in, user_id=current_user.id)

@router.get("/", response_model=List[ProjectRead])
def read_projects(current_user: CurrentUser, service: ProjectService = Depends(get_project_service)):
    return service.get_user_projects(user_id=current_user.id)