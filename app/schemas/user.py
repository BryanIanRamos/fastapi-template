from pydantic import BaseModel, EmailStr
from datetime import datetime
from uuid import UUID


class UserBase(BaseModel):
    """Base user schema"""
    email: EmailStr
    first_name: str | None = None
    last_name: str | None = None


class UserCreate(UserBase):
    """User creation schema"""
    username: str
    password: str


class UserUpdate(BaseModel):
    """User update schema"""
    email: EmailStr | None = None
    first_name: str | None = None
    last_name: str | None = None


class UserRead(UserBase):
    """User read schema"""
    user_id: UUID
    username: str
    is_active: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
