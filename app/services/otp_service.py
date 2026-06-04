from datetime import datetime, timedelta
import random
import string
from sqlalchemy.orm import Session
from app.models.otp_token import OTPToken
from app.services.email_service import send_email

class OTPService:
    """Service for managing One-Time Passwords (OTP)"""
    
    OTP_EXPIRY_MINUTES = 5

    @staticmethod
    def generate_otp(email: str, purpose: str, db: Session) -> str:
        """
        Generate a 6-digit OTP, save it to DB, and send it via email.
        Purpose should be 'registration' or 'password_reset'.
        """
        # Generate 6-digit random number
        otp = ''.join(random.choices(string.digits, k=6))
        
        # Invalidate any existing unused OTPs for this email and purpose
        db.query(OTPToken).filter(
            OTPToken.email == email, 
            OTPToken.purpose == purpose, 
            OTPToken.is_used == False
        ).update({"is_used": True})
        
        # Save new OTP
        expires_at = datetime.utcnow() + timedelta(minutes=OTPService.OTP_EXPIRY_MINUTES)
        otp_record = OTPToken(
            email=email,
            token=otp,
            expires_at=expires_at,
            purpose=purpose
        )
        db.add(otp_record)
        db.commit()
        db.refresh(otp_record)

        # Send email
        subject = "Your Verification Code" if purpose == 'registration' else "Password Reset Code"
        body = f"Your verification code is: {otp}\nIt will expire in {OTPService.OTP_EXPIRY_MINUTES} minutes."
        
        try:
            send_email(to=email, subject=subject, body=body)
        except Exception as e:
            # We still return the OTP for testing purposes, but in production 
            # you might want to raise an exception here.
            print(f"Email failed: {e}")

        return otp

    @staticmethod
    def verify_otp(email: str, token: str, purpose: str, db: Session) -> bool:
        """
        Verify if the provided OTP is correct, not expired, and not used.
        """
        record = db.query(OTPToken).filter(
            OTPToken.email == email,
            OTPToken.token == token,
            OTPToken.purpose == purpose,
            OTPToken.is_used == False,
            OTPToken.expires_at > datetime.utcnow()
        ).first()

        if not record:
            return False

        # Mark as used
        record.is_used = True
        db.commit()
        return True
