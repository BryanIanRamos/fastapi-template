from datetime import datetime
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from app.models.token import Token


class TokenService:
    """Token business logic service"""

    @staticmethod
    def save_token(db: Session, user_id: UUID, token_string: str, expires_at: datetime) -> Token:
        """Save token to database"""
        try:
            db_token = Token(
                user_id=user_id,
                token=token_string,
                expires_at=expires_at,
            )
            db.add(db_token)
            db.commit()
            db.refresh(db_token)
            return db_token
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Error saving token",
            )

    @staticmethod
    def get_token_by_string(db: Session, token_string: str) -> Token | None:
        """Get token record by token string"""
        return db.query(Token).filter(
            Token.token == token_string,
            Token.revoked == False
        ).first()

    @staticmethod
    def revoke_token(db: Session, token_string: str) -> bool:
        """Revoke a token"""
        token = db.query(Token).filter(Token.token == token_string).first()
        if not token:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Token not found",
            )
        
        token.revoked = True
        db.add(token)
        db.commit()
        return True

    @staticmethod
    def is_token_revoked(db: Session, token_string: str) -> bool:
        """Check if token is revoked"""
        token = db.query(Token).filter(Token.token == token_string).first()
        if not token:
            return True  # Non-existent tokens are considered revoked
        return token.revoked

    @staticmethod
    def revoke_user_tokens(db: Session, user_id: UUID) -> bool:
        """Revoke all tokens for a user"""
        try:
            db.query(Token).filter(Token.user_id == user_id).update(
                {Token.revoked: True}
            )
            db.commit()
            return True
        except Exception:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Error revoking tokens",
            )
