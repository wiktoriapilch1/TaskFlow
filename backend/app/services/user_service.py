from sqlmodel import Session, select
from app.core.exceptions import InternalServerError, InvalidCredentialsException, UserAlreadyExistsException
from app.core.security import get_password_hash, verify_password
from app.models.user import ROLE_USER, User
from app.schemas.user import UserCreate, UserUpdate
import logging

logger = logging.getLogger(__name__)

class UserService():
    def __init__(self, session: Session):
        self.session = session

    def get_by_email(self, email: str) -> User | None:
        query = select(User).where(User.email == email)
        return self.session.exec(query).first()

    def create_user(self, user_in: UserCreate) -> User:
        if self.get_by_email(user_in.email):
            logger.warning(f"User {user_in.email} already exists")
            raise UserAlreadyExistsException()
        
        user = User (
            email = user_in.email,
            hashed_password = get_password_hash(user_in.password),
            is_active = True,
            role = ROLE_USER
        )
        
        try: 
            self.session.add(user)
            self.session.commit()
            self.session.refresh(user)
        except Exception as e:
            logger.exception(f"Critical database error while creating user: {user_in.email}")
            self.session.rollback()
            raise InternalServerError
        
        logger.info(f"User {user_in.email} created successfully")
        return user
    
    def update_user(self, *, current_user: User, user_in: UserUpdate) -> User:
        if user_in.email is not None and user_in.email != current_user.email:
            if self.get_by_email(user_in.email):
                raise UserAlreadyExistsException()
            current_user.email = user_in.email
            if user_in.password is not None:
                current_user.hashed_password = get_password_hash(user_in.password)
            self.session.add(current_user)
            self.session.commit()
            self.session.refresh(current_user)
            return current_user

    def authenticate(self, email: str, password: str) -> User:
        query = select(User).where(User.email == email)
        user = self.session.exec(query).first()
        if not user or not verify_password(password, user.hashed_password):
            logger.warning(f"Log in failed for: {email}")
            raise InvalidCredentialsException
        logger.info(f"User {user.email} successfully logged in (ID: {user.id})")
        return user