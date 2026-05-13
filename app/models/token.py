from uuid import uuid4
from sqlalchemy import Column, DateTime, Boolean, ForeignKey, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.base import Base


class Token(Base):
    """Token model - Authentication tokens for users"""
    __tablename__ = "tokens"

    token_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False, index=True)
    token = Column(String, nullable=False, unique=True, index=True)  # JWT token string
    expires_at = Column(DateTime(timezone=True), nullable=False)
    revoked = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationship
    user = relationship("User", backref="tokens")

    def __repr__(self):
        return f"<Token(token_id={self.token_id}, user_id={self.user_id})>"
