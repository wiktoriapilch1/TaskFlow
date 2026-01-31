from sqlmodel import Session, select
from app.core.exceptions import InvalidCredentialsException, UserAlreadyExistsException
from app.core.security import get_password_hash, verify_password
from app.models.users import ROLE_USER, User
from app.schemas.user import UserCreate
import logging

logger = logging.getLogger(__name__)

class UserService():
    def __init__(self, session: Session):
        self.session = session

    def create_user(self, user_in: UserCreate) -> User:
        query = select(User).where(User.email == user_in.email)
        if self.session.exec(query).first():
            logger.info(f"User {user_in.email} already exists")
            raise UserAlreadyExistsException()
        
        user = User (
            email = user_in.email,
            hashed_password = get_password_hash(user_in.password),
            is_active = True,
            role = ROLE_USER
        )

        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)

        return user
    
    def authenticate(self, email: str, password: str) -> User:
        query = select(User).where(User.email == email)
        user = self.session.exec(query).first()
        if not user or not verify_password(password, user.hashed_password):
            logger.info(f"Log in failed for: {email}")
            raise InvalidCredentialsException
        logger.info(f"User {user.email} successfully logged in (ID: {user.id})")
        return user