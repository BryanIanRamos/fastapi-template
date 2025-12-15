from pydantic import BaseModel, EmailStr


class UserLogin(BaseModel):
    """User login schema"""
    email: EmailStr
    password: str


class UserRegister(BaseModel):
    """User registration schema"""
    email: EmailStr
    password: str
    full_name: str | None = None


class Token(BaseModel):
    """JWT token response schema"""
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Token payload data"""
    email: str | None = None
