from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr


class SystemUserBase(BaseModel):
    email: EmailStr
    role: int = 0
    admin: UUID | None = None
    acad_info_id: UUID | None = None
    forwarded_by: UUID | None = None


class SystemUserCreate(SystemUserBase):
    model_config = ConfigDict(extra='forbid')
    
    password: str
    verified_at: datetime | None = None


class SystemUserUpdate(BaseModel):
    model_config = ConfigDict(extra='forbid')
    
    email: EmailStr | None = None
    password: str | None = None
    verified_at: datetime | None = None
    role: int | None = None
    admin: UUID | None = None
    acad_info_id: UUID | None = None
    forwarded_by: UUID | None = None


class SystemUserRead(SystemUserBase):
    user_id: UUID
    verified_at: datetime | None
    created_at: datetime

    class Config:
        from_attributes = True
