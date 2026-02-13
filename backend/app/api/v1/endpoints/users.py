from fastapi import APIRouter, Depends

from app.api.deps import CurrentUser, get_user_service
from app.schemas.user import UserRead, UserUpdate
from app.services.user_service import UserService

router = APIRouter()

@router.get("/me", response_model=UserRead)
def read_user_me(current_user: CurrentUser):
    return current_user

@router.patch("/me", response_model=UserRead)
def update_user(*, user_in: UserUpdate, current_user: CurrentUser, service: UserService = Depends(get_user_service)):
    return service.update_user(current_user=current_user, user_in=user_in)