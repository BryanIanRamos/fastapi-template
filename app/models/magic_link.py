from sqlalchemy import Column, String, DateTime, Boolean, Integer
from sqlalchemy.sql import func
from app.db.base import Base


class MagicLinkToken(Base):
    __tablename__ = "magic_link_tokens"

    id = Column(Integer, primary_key=True, index=True)

    email = Column(String, index=True, nullable=False)

    token_hash = Column(String, unique=True, nullable=False)

    expires_at = Column(DateTime, nullable=False)

    used = Column(Boolean, default=False)

    created_at = Column(DateTime, server_default=func.now())