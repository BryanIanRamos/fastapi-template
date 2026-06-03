from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from app.models.magic_link import MagicLinkToken
from app.core.security import (
    generate_magic_token,
    hash_token,
    verify_token
)
from app.services.email_service import send_email


MAGIC_LINK_EXPIRY_MINUTES = 15


def create_magic_link(db: Session, email: str, base_url: str):
    token = generate_magic_token()
    token_hash = hash_token(token)

    record = MagicLinkToken(
        email=email,
        token_hash=token_hash,
        expires_at=datetime.utcnow() + timedelta(minutes=MAGIC_LINK_EXPIRY_MINUTES),
    )

    db.add(record)
    db.commit()

    link = f"{base_url}/auth/verify-magic-link?token={token}"

    try:
        send_email(
            to=email,
            subject="Your Magic Login Link",
            body=f"Click to login: {link}\nThis link expires in 15 minutes."
        )
    except Exception as e:
        return {"message": f"Failed to send magic link: {str(e)}", "success": False}

    return {"message": "Magic link sent successfully", "success": True}


def verify_magic_link(db: Session, token: str):
    token_hash = hash_token(token)

    record = (
        db.query(MagicLinkToken)
        .filter(
            MagicLinkToken.token_hash == token_hash,
            MagicLinkToken.used == False
        )
        .first()
    )

    if not record:
        return None

    if record.expires_at < datetime.utcnow():
        return None

    # mark as used
    record.used = True
    db.commit()

    return record.email