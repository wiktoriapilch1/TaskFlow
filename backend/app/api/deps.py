import logging
from typing import Annotated
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import ValidationError
from sqlmodel import Session
from app.core.config import settings
from app.db.session import get_session
from app.models.user import User
from app.core.security import ALGORITHM
from app.core.exceptions import JWTException, UserInactiveException, UserNotFoundException
from app.services.user_service import UserService

logger = logging.getLogger(__name__)
reusable_oauth2 = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")

def get_user_service(session: Session = Depends(get_session)) -> UserService:
    return UserService(session)

def get_current_user(session: Session = Depends(get_session), token: str = Depends(reusable_oauth2)) -> User:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        token_data = payload.get("sub")
        if token_data is None:
            logger.exception(f"Could not validate credentials")
            session.rollback()
            raise JWTException()
        token_id = int(token_data)
    except (JWTError, ValidationError):
        raise JWTException()
    user = session.get(User, token_id)
    if not user:
        raise UserNotFoundException()
    if not user.is_active:
        raise UserInactiveException()
    return user

CurrentUser = Annotated[User, Depends(get_current_user)]