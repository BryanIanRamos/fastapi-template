from pydantic import BaseModel, ConfigDict, EmailStr


class UserLogin(BaseModel):
    """User login schema"""
    model_config = ConfigDict(extra='forbid')
    
    email: EmailStr
    password: str


class UserRegister(BaseModel):
    """User registration schema"""
    model_config = ConfigDict(extra='forbid')
    
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
