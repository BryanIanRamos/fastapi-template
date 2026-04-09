import uuid

from sqlalchemy import Column, DateTime, ForeignKey, String, Uuid, func
from sqlalchemy.orm import relationship

from app.models.custom_base import SystemBase


class SystemToken(SystemBase):
    __tablename__ = "tokens"

    token_id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    value = Column(String(100), nullable=False)
    expired_at = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    user_id = Column(Uuid, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False, index=True)

    user = relationship("SystemUser", back_populates="tokens")
