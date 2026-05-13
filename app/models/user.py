from uuid import uuid4
from sqlalchemy import Column, String, DateTime, Integer, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import UUID
from app.db.base import Base


class User(Base):
    """User model"""
    __tablename__ = "users"
    __table_args__ = (
        UniqueConstraint("email", name="uq_users_email"),
        UniqueConstraint("username", name="uq_users_username"),
    )

    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, nullable=False, unique=True)
    username = Column(String(255), nullable=False, unique=True, index=True)
    email = Column(String(100), nullable=False, index=True)
    password = Column(String, nullable=False)
    first_name = Column(String(255), nullable=True)
    last_name = Column(String(255), nullable=True)
    is_active = Column(Integer, default=1, nullable=False)
    role = Column(Integer, nullable=True, comment="Account role")
    verified_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    def __repr__(self):
        return f"<User(user_id={self.user_id}, username={self.username}, email={self.email})>"
