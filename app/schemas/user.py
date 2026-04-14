from pydantic import BaseModel, ConfigDict, EmailStr
from datetime import datetime


class UserBase(BaseModel):
    """Base user schema"""
    email: EmailStr
    full_name: str | None = None


class UserCreate(UserBase):
    """User creation schema"""
    model_config = ConfigDict(extra='forbid')
    
    password: str


class UserUpdate(BaseModel):
    """User update schema"""
    model_config = ConfigDict(extra='forbid')
    
    email: EmailStr | None = None
    full_name: str | None = None


class UserRead(UserBase):
    """User read schema"""
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
