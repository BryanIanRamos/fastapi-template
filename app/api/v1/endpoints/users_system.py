import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, ConfigDict, EmailStr
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.api.response import pagination_meta, success_response
from app.api.v1.endpoints.auth_system import get_current_system_user
from app.core.security import hash_password
from app.models.users import SystemUser

router = APIRouter()


class CreateUserRequest(BaseModel):
    model_config = ConfigDict(extra='forbid')
    
    fullName: str
    email: EmailStr
    role: int


class UpdateUserRequest(BaseModel):
    model_config = ConfigDict(extra='forbid')
    
    email: EmailStr | None = None
    role: int | None = None


def _status(user: SystemUser) -> str:
    return "active" if user.verified_at else "pending-email"


def _user_payload(user: SystemUser) -> dict:
    full_name = user.email.split("@")[0].replace(".", " ").title()
    return {
        "fullName": full_name,
        "email": user.email,
        "role": user.role,
        "status": _status(user),
        "createdAt": user.created_at.isoformat() if user.created_at else None,
    }


@router.get("/")
def list_users(
    page: int = Query(default=1, ge=1),
    pageSize: int = Query(default=20, ge=1, le=100),
    search: str | None = None,
    role: int | None = None,
    status_filter: str | None = Query(default=None, alias="status"),
    db: Session = Depends(get_db),
    _: SystemUser = Depends(get_current_system_user),
):
    query = db.query(SystemUser)

    if search:
        query = query.filter(SystemUser.email.ilike(f"%{search}%"))
    if role:
        query = query.filter(SystemUser.role == role)
    if status_filter == "active":
        query = query.filter(SystemUser.verified_at.isnot(None))
    elif status_filter == "pending-email":
        query = query.filter(SystemUser.verified_at.is_(None))

    total = query.count()
    items = (
        query.order_by(SystemUser.created_at.desc())
        .offset((page - 1) * pageSize)
        .limit(pageSize)
        .all()
    )

    return success_response("OK", [_user_payload(item) for item in items], pagination_meta(page, pageSize, total))


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(payload: CreateUserRequest, db: Session = Depends(get_db), _: SystemUser = Depends(get_current_system_user)):
    existing = db.query(SystemUser).filter(SystemUser.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    temp_password = str(uuid.uuid4())[:10]
    user = SystemUser(
        email=payload.email,
        password=hash_password(temp_password),
        role=payload.role,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    data = _user_payload(user)
    data["temporaryPassword"] = temp_password
    return success_response("User created", data)


@router.get("/{user_id}")
def get_user(user_id: uuid.UUID, db: Session = Depends(get_db), _: SystemUser = Depends(get_current_system_user)):
    user = db.query(SystemUser).filter(SystemUser.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return success_response("OK", _user_payload(user))


@router.patch("/{user_id}")
def update_user(
    user_id: uuid.UUID,
    payload: UpdateUserRequest,
    db: Session = Depends(get_db),
    _: SystemUser = Depends(get_current_system_user),
):
    user = db.query(SystemUser).filter(SystemUser.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if payload.email is not None:
        user.email = payload.email
    if payload.role is not None:
        user.role = payload.role

    db.add(user)
    db.commit()
    db.refresh(user)

    return success_response("User updated", _user_payload(user))


@router.post("/{user_id}/resend-invite")
def resend_invite(user_id: uuid.UUID, db: Session = Depends(get_db), _: SystemUser = Depends(get_current_system_user)):
    user = db.query(SystemUser).filter(SystemUser.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return success_response("Invite resent", {"email": user.email})


@router.patch("/{user_id}/verify")
def verify_user(user_id: uuid.UUID, db: Session = Depends(get_db), _: SystemUser = Depends(get_current_system_user)):
    user = db.query(SystemUser).filter(SystemUser.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    from datetime import datetime

    user.verified_at = datetime.utcnow()
    db.add(user)
    db.commit()
    db.refresh(user)

    return success_response("User verified", _user_payload(user))
