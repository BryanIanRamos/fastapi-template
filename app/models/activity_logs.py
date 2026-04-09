import uuid

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Uuid, func
from sqlalchemy.orm import relationship

from app.models.custom_base import SystemBase


class ActivityLog(SystemBase):
    __tablename__ = "activity_log"

    log_id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    user_name = Column(String(100), nullable=False)
    user_role = Column(Integer, nullable=False)
    module = Column(String(100), nullable=False)
    recorded = Column(String(255), nullable=False)
    happended_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    user_id = Column(Uuid, ForeignKey("users.user_id", ondelete="SET NULL"), nullable=True, index=True)

    user = relationship("SystemUser", back_populates="activity_logs")
