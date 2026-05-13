from uuid import uuid4
from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.base import Base


class Session(Base):
    """Session model - User device/login sessions"""
    __tablename__ = "sessions"

    session_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False, index=True)
    token_id = Column(UUID(as_uuid=True), ForeignKey("tokens.token_id"), nullable=False, index=True)
    device_name = Column(String(255), nullable=True, comment="Logged in devices")
    user_agent = Column(Text, nullable=True)
    ip_address = Column(String(45), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    last_active = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationships
    user = relationship("User", backref="sessions")
    token = relationship("Token", backref="sessions")

    def __repr__(self):
        return f"<Session(session_id={self.session_id}, user_id={self.user_id})>"
