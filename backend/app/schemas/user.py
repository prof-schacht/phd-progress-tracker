from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr
from app.models.user import UserRole, UserStatus


class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    role: UserRole = UserRole.STUDENT
    status: UserStatus = UserStatus.ACTIVE


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    role: Optional[UserRole] = None
    status: Optional[UserStatus] = None
    password: Optional[str] = None


class UserInDBBase(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime
    last_login: Optional[datetime] = None

    class Config:
        from_attributes = True


class User(UserInDBBase):
    pass


class UserInDB(UserInDBBase):
    hashed_password: str


class UserProfileBase(BaseModel):
    department: Optional[str] = None
    phone: Optional[str] = None
    office_location: Optional[str] = None
    bio: Optional[str] = None
    avatar_url: Optional[str] = None
    timezone: str = "UTC"


class UserProfileCreate(UserProfileBase):
    pass


class UserProfileUpdate(UserProfileBase):
    pass


class UserProfile(UserProfileBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True