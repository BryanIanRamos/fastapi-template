import uuid

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Uuid, func
from sqlalchemy.orm import relationship

from app.models.custom_base import SystemBase


class SystemUser(SystemBase):
    __tablename__ = "users"

    user_id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    email = Column(String(100), nullable=False, unique=True, index=True)
    password = Column(String(100), nullable=False)
    vertified_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    role = Column(Integer, default=0, nullable=False)
    admin = Column(Uuid, ForeignKey("users.user_id"), nullable=True)
    acad_info_id = Column(Uuid, nullable=True)
    forwarded_by = Column(Uuid, ForeignKey("users.user_id"), nullable=True)

    tokens = relationship("SystemToken", back_populates="user", cascade="all, delete-orphan")
    activity_logs = relationship("ActivityLog", back_populates="user")
