from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class ActivityLogBase(BaseModel):
    user_name: str
    user_role: int
    module: str
    recorded: str
    user_id: UUID | None = None


class ActivityLogCreate(ActivityLogBase):
    happended_at: datetime | None = None


class ActivityLogUpdate(BaseModel):
    user_name: str | None = None
    user_role: int | None = None
    module: str | None = None
    recorded: str | None = None
    happended_at: datetime | None = None
    user_id: UUID | None = None


class ActivityLogRead(ActivityLogBase):
    log_id: UUID
    happended_at: datetime

    class Config:
        from_attributes = True
