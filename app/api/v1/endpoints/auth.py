from datetime import timedelta, datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional

from app.api.deps import get_db
from app.core.security import create_access_token, decode_access_token
from app.core.config import settings
from app.schemas.auth import Token, UserLogin, UserRegister
from app.schemas.user import UserRead
from app.services.user_service import UserService
from app.services.token_service import TokenService
from app.services.auth_service import create_magic_link, verify_magic_link
from app.services.otp_service import OTPService
from app.models.user import User
from app.schemas.auth import Token, UserLogin, UserRegister
from app.schemas.user import UserRead
from app.services.user_service import UserService
from app.services.token_service import TokenService
from app.services.auth_service import create_magic_link, verify_magic_link
from app.services.otp_service import OTPService
from app.models.user import User

router = APIRouter()

# class MagicLinkRequest(BaseModel):
#     email: str

class OTPRequest(BaseModel):
    email: str
    purpose: str # 'registration' or 'password_reset'

class OTPVerifyRequest(BaseModel):
    email: str
    token: str
    purpose: str # 'registration' or 'password_reset'
    password: Optional[str] = None # Required for password reset

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    """Get current authenticated user from JWT token"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    # Check if token is revoked
    if TokenService.is_token_revoked(db, token):
        raise credentials_exception
    
    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception
    
    email: str = payload.get("sub")
    if email is None:
        raise credentials_exception
    
    user = UserService.get_user_by_email(db, email=email)
    if user is None:
        raise credentials_exception
    
    return user


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register(
    user_in: UserRegister,
    db: Session = Depends(get_db),
):
    """
    Register a new user
    
    - **email**: Valid email address
    - **username**: Unique username
    - **password**: User password (will be hashed automatically)
    - **first_name**: Optional first name
    - **last_name**: Optional last name

    Example:
        POST /api/v1/auth/register
        {
            "email": "user@example.com",
            "username": "johndoe",
            "password": "securepassword123",
            "first_name": "John",
            "last_name": "Doe"
        }
    """
    from app.schemas.user import UserCreate
    
    user_create = UserCreate(
        email=user_in.email,
        username=user_in.username,
        password=user_in.password,
        first_name=user_in.first_name,
        last_name=user_in.last_name
    )
    
    user = UserService.create_user(db, user_create)
    return user


@router.post("/login", response_model=Token)
def login(
    user_credentials: UserLogin,
    db: Session = Depends(get_db),
):
    """
    Login with email and password
    
    - **email**: User email address
    - **password**: User password

    Returns JWT access token for authentication

    Example:
        POST /api/v1/auth/login
        {
            "email": "user@example.com",
            "password": "securepassword123"
        }
    """
    user = UserService.authenticate_user(db, user_credentials.email, user_credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    
    # Save token to database
    expires_at = datetime.now(timezone.utc) + access_token_expires
    TokenService.save_token(db, user.user_id, access_token, expires_at)
    
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/login/form", response_model=Token)
def login_form(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    """
    OAuth2 compatible login (for Swagger UI docs)
    
    Uses form data instead of JSON - username field accepts email or username

    Example:
        POST /api/v1/auth/login/form
        Form Data:
            username: "user@example.com"
            password: "securepassword123"
    """
    # Try to authenticate with email or username
    user = UserService.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    
    # Save token to database
    expires_at = datetime.now(timezone.utc) + access_token_expires
    TokenService.save_token(db, user.user_id, access_token, expires_at)
    
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=UserRead)
def get_me(current_user: User = Depends(get_current_user)):
    """
    Get current authenticated user
    
    Requires valid JWT token in Authorization header

    Example:
        GET /api/v1/auth/me
        Header: Authorization: Bearer <your_token_here>
    """
    return current_user


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    """
    Logout - revoke the current token
    
    Requires valid JWT token in Authorization header

    Example:
        POST /api/v1/auth/logout
        Header: Authorization: Bearer <your_token_here>
    """
    TokenService.revoke_token(db, token)
    return None


@router.post("/otp/request")
def request_otp(
    request: OTPRequest,
    db: Session = Depends(get_db)
):
    """
    Request an OTP for registration or password reset
    
    - **email**: Valid email address
    - **purpose**: 'registration' or 'password_reset'

    Example:
        POST /api/v1/auth/otp/request
        {
            "email": "user@example.com",
            "purpose": "registration"
        }
    """
    if request.purpose not in ['registration', 'password_reset']:
        raise HTTPException(status_code=400, detail="Invalid purpose. Use 'registration' or 'password_reset'")
    
    otp = OTPService.generate_otp(request.email, request.purpose, db)
    return {"message": f"OTP sent to {request.email} for {request.purpose}"}


@router.post("/otp/verify")
def verify_otp(
    request: OTPVerifyRequest,
    db: Session = Depends(get_db)
):
    """
    Verify OTP and perform action (registration or password reset)
    
    - **email**: User email address
    - **token**: The OTP token received
    - **purpose**: 'registration' or 'password_reset'
    - **password**: Required if purpose is 'password_reset'

    Example:
        POST /api/v1/auth/otp/verify
        {
            "email": "user@example.com",
            "token": "123456",
            "purpose": "password_reset",
            "password": "newsecurepassword123"
        }
    """
    is_valid = OTPService.verify_otp(request.email, request.token, request.purpose, db)
    
    if not is_valid:
        raise HTTPException(status_code=400, detail="Invalid or expired OTP")

    if request.purpose == 'password_reset':
        if not request.password:
            raise HTTPException(status_code=400, detail="Password is required for password reset")
        
        user = UserService.get_user_by_email(db, email=request.email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        UserService.update_password(db, user, request.password)
        return {"message": "Password has been successfully reset"}

    if request.purpose == 'registration':
        return {"message": "OTP verified. You can now proceed to complete registration."}

    return {"message": "OTP verified successfully"}
