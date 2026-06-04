from datetime import timedelta, datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.api.deps import get_db
from app.core.security import create_access_token, decode_access_token
from app.core.config import settings
from app.schemas.auth import Token, UserLogin, UserRegister
from app.schemas.user import UserRead
from app.services.user_service import UserService
from app.services.token_service import TokenService
from app.services.auth_service import create_magic_link, verify_magic_link
from app.models.user import User
from app.schemas.auth import Token, UserLogin, UserRegister
from app.schemas.user import UserRead
from app.services.user_service import UserService
from app.services.token_service import TokenService
from app.services.auth_service import create_magic_link, verify_magic_link
from app.models.user import User

router = APIRouter()

# class MagicLinkRequest(BaseModel):
#     email: str

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
    """
    TokenService.revoke_token(db, token)
    return None


# @router.post("/magic-link", response_model=dict)
# def request_magic_link(
#     request: MagicLinkRequest, 
#     db: Session = Depends(get_db)
# ):
#     """
#     Request a passwordless magic link login
#     
#     - **email**: User's email address
#     
#     Example:
#         POST /api/v1/auth/magic-link
#         {
#             "email": "user@example.com"
#         }
#     """
#     # Use the base URL from settings if available, otherwise fallback to localhost
#     base_url = getattr(settings, "BASE_URL", "http://localhost:8000")
#     return create_magic_link(db, request.email, base_url)


# @router.get("/verify-magic-link", response_model=Token)
# def verify_magic_link_route(
#     token: str, 
#     db: Session = Depends(get_db)
# ):
#     """
#     Verify magic link and redirect to frontend with JWT
#     
#     - **token**: The secure token from the email link
#     
#     Example:
#         GET /api/v1/auth/verify-magic-link?token=xyz123...
#     """
#     email = verify_magic_link(db, token)
# 
#     if not email:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST, 
#             detail="Invalid or expired magic link"
#         )
# 
#     # Generate JWT access token
#     access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = create_access_token(
#         data={"sub": email}, 
#         expires_delta=access_token_expires
#     )
# 
#     # Save token to database for tracking/revocation
#     user = UserService.get_user_by_email(db, email=email)
#     if user:
#         expires_at = datetime.now(timezone.utc) + access_token_expires
#         TokenService.save_token(db, user.user_id, access_token, expires_at)
# 
#     # Redirect to frontend with token in query parameter
#     # frontend_url = getattr(settings, "FRONTEND_URL", "http://localhost:3000/auth-callback")
#     frontend_url = getattr(settings, "FRONTEND_URL", "https://bryan-ramos-phi.vercel.app/")
#     redirect_url = f"{frontend_url}?token={access_token}"
#     
#     return RedirectResponse(url=redirect_url)
