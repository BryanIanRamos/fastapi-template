from pydantic import BaseModel, ConfigDict
from datetime import datetime


class TaskBase(BaseModel):
    """Base task schema with common fields"""
    title: str
    description: str | None = None
    status: str = "pending"


class TaskCreate(TaskBase):
    """Schema for creating a task"""
    model_config = ConfigDict(extra='forbid')


class TaskUpdate(BaseModel):
    """Schema for updating a task - all fields optional"""
    model_config = ConfigDict(extra='forbid')
    
    title: str | None = None
    description: str | None = None
    status: str | None = None


class TaskRead(TaskBase):
    """Schema for reading a task - includes DB fields"""
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
