from sqlalchemy import Column, String, DateTime, Boolean, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base
from sqlalchemy.dialects.postgresql import UUID


class MagicLinkToken(Base):
    __tablename__ = "magic_link_tokens"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=True)
    email = Column(String, index=True, nullable=False)

    token_hash = Column(String, unique=True, nullable=False)

    expires_at = Column(DateTime, nullable=False)

    used = Column(Boolean, default=False)

    created_at = Column(DateTime, server_default=func.now())

    user = relationship("User", back_populates="magic_links")