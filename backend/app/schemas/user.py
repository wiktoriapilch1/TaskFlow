from typing import Literal, Optional
from pydantic import BaseModel, EmailStr

RoleType = Literal["admin", "user"]

class UserBase(BaseModel):
    email: EmailStr
    is_active: bool

class UserCreate(UserBase):
    password: str

class UserRead(UserBase):
    id: int
    role: RoleType

class UserUpdate(UserBase):
    email: Optional[EmailStr] = None
    password: Optional[str] = None

class AuthResponse(BaseModel):
    user: UserRead
    access_token: str
    refresh_token: str
    token_type: str = "bearer"