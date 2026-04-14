import uuid
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.api.response import success_response
from app.core.config import settings
from app.core.security import create_access_token, decode_access_token, hash_password, verify_password
from app.models.tokens import SystemToken
from app.models.users import SystemUser

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    token: str
    newPassword: str


def _role_label(role_value: int) -> str:
    return "admin" if role_value == 1 else "field-personnel"


def _user_payload(user: SystemUser) -> dict:
    full_name = user.email.split("@")[0].replace(".", " ").title()
    return {
        "id": str(user.user_id),
        "fullName": full_name,
        "position": "N/A",
        "email": user.email,
        "role": _role_label(user.role),
    }


async def get_current_system_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> SystemUser:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception

    subject = payload.get("sub")
    if subject is None:
        raise credentials_exception

    try:
        user_id = uuid.UUID(subject)
    except ValueError as exc:
        raise credentials_exception from exc

    user = db.query(SystemUser).filter(SystemUser.user_id == user_id).first()
    if user is None:
        raise credentials_exception

    return user


@router.post("/login")
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(SystemUser).filter(SystemUser.email == payload.email).first()
    if not user or not verify_password(payload.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")

    access_token = create_access_token(
        data={"sub": str(user.user_id)},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    refresh_token = str(uuid.uuid4())

    db_token = SystemToken(
        token_type="refresh",
        value=refresh_token,
        expired_at=datetime.utcnow() + timedelta(days=7),
        user_id=user.user_id,
    )
    db.add(db_token)
    db.commit()

    return success_response(
        "OK",
        {
            "accessToken": access_token,
            "refreshToken": refresh_token,
            "user": _user_payload(user),
        },
    )


@router.get("/me")
def get_me(current_user: SystemUser = Depends(get_current_system_user)):
    return success_response("OK", _user_payload(current_user))


@router.post("/logout")
def logout(current_user: SystemUser = Depends(get_current_system_user), db: Session = Depends(get_db)):
    db.query(SystemToken).filter(SystemToken.user_id == current_user.user_id).delete()
    db.commit()
    return success_response("Logged out", {"ok": True})


@router.post("/forgot-password")
def forgot_password(payload: ForgotPasswordRequest, db: Session = Depends(get_db)):
    user = db.query(SystemUser).filter(SystemUser.email == payload.email).first()
    if user:
        reset_token = str(uuid.uuid4())
        db_token = SystemToken(
            token_type="reset",
            value=reset_token,
            expired_at=datetime.utcnow() + timedelta(hours=1),
            user_id=user.user_id,
        )
        db.add(db_token)
        db.commit()

    return success_response("If the email exists, a reset token was generated", {"ok": True})


@router.post("/reset-password")
def reset_password(payload: ResetPasswordRequest, db: Session = Depends(get_db)):
    token_row = (
        db.query(SystemToken)
        .filter(SystemToken.value == payload.token, SystemToken.expired_at >= datetime.utcnow())
        .first()
    )
    if token_row is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or expired token")

    user = db.query(SystemUser).filter(SystemUser.user_id == token_row.user_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    user.password = hash_password(payload.newPassword)
    db.delete(token_row)
    db.add(user)
    db.commit()

    return success_response("Password reset successful", {"ok": True})
