from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session

from app.core.security import create_access_token, create_refresh_token
from app.db.session import get_session
from app.schemas.user import AuthResponse, UserCreate
from app.services.user_service import UserService

router = APIRouter()

def get_user_service(session: Session = Depends(get_session)) -> UserService:
    return UserService(session)

@router.post("/register", response_model=AuthResponse, status_code=201)
def register(user_in: UserCreate, service: UserService = Depends(get_user_service)):
    user = service.create_user(user_in)
    return {
        "user": user,
        "access_token": create_access_token(user.id),
        "refresh_token": create_refresh_token(user.id)
    }

@router.post("/login", response_model=AuthResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends(), service: UserService = Depends(get_user_service)):
    user = service.authenticate(email=form_data.username, password=form_data.password)
    return {
        "user": user,
        "access_token": create_access_token(user.id),
        "refresh_token": create_refresh_token(user.id)
    }