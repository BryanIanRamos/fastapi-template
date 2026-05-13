from pydantic import BaseModel
from datetime import datetime
from uuid import UUID


class TaskBase(BaseModel):
    """Base task schema with common fields"""
    title: str
    description: str | None = None
    status: str = "pending"


class TaskCreate(TaskBase):
    """Schema for creating a task"""
    pass


class TaskUpdate(BaseModel):
    """Schema for updating a task - all fields optional"""
    title: str | None = None
    description: str | None = None
    status: str | None = None


class TaskRead(TaskBase):
    """Schema for reading a task - includes DB fields"""
    id: int
    user_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
