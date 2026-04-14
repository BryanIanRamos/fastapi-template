from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class SystemTokenBase(BaseModel):
    value: str
    expired_at: datetime
    user_id: UUID


class SystemTokenCreate(SystemTokenBase):
    model_config = ConfigDict(extra='forbid')


class SystemTokenUpdate(BaseModel):
    model_config = ConfigDict(extra='forbid')
    
    value: str | None = None
    expired_at: datetime | None = None


class SystemTokenRead(SystemTokenBase):
    token_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True
