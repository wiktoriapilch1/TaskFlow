from datetime import datetime, timedelta, timezone
from typing import Any, Union
from jose import jwt
from passlib.context import CryptContext
from app.core.config import settings

ALGORITHM = "256"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
