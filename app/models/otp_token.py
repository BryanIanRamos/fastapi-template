from sqlalchemy import Column, String, Integer, DateTime, Boolean, func, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base
from sqlalchemy.dialects.postgresql import UUID

class OTPToken(Base):
    """OTP Token model for email verification and password resets"""
    __tablename__ = "otp_tokens"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=True)
    email = Column(String(100), nullable=False, index=True)
    token = Column(String(6), nullable=False) # 6-digit OTP
    expires_at = Column(DateTime(timezone=True), nullable=False)
    is_used = Column(Boolean, default=False, nullable=False)
    purpose = Column(String(20), nullable=False) # 'registration' or 'password_reset'
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    user = relationship("User", back_populates="otp_tokens")

    def __repr__(self):
        return f"<OTPToken(email={self.email}, token={self.token}, purpose={self.purpose})>"
