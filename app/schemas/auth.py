from pydantic import BaseModel, EmailStr
from datetime import datetime
from uuid import UUID


class UserLogin(BaseModel):
    """User login schema"""
    email: EmailStr
    password: str


class UserRegister(BaseModel):
    """User registration schema"""
    email: EmailStr
    username: str
    password: str
    first_name: str | None = None
    last_name: str | None = None


class Token(BaseModel):
    """JWT token response schema"""
    access_token: str
    token_type: str = "bearer"


class TokenRead(BaseModel):
    """Token read schema - for retrieving tokens from DB"""
    token_id: UUID
    user_id: UUID
    token: str
    expires_at: datetime
    revoked: bool
    created_at: datetime

    class Config:
        from_attributes = True


class TokenData(BaseModel):
    """Token payload data"""
    email: str | None = None
