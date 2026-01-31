from datetime import datetime, timedelta, timezone
from typing import Any
from jose import jwt
from passlib.context import CryptContext
from app.core.config import settings

ALGORITHM = "HS256"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def _create_token(subject: str|int, expires_delta: timedelta, type: str):
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode = {
        "exp": expire,
        "sub": str(subject),
        "type": type
    }
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_access_token(subject: str|int) -> str:
    expires_delta = timedelta(minutes=1)
    return _create_token(subject, expires_delta, type="access")

def create_refresh_token(subject: str|int) -> str:
    expires_delta = timedelta(days=7)
    return _create_token(subject, expires_delta, type="refresh")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password) 

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
