from datetime import datetime, timedelta
import jwt

SECRET_KEY = "super-secret"
ALGORITHM = "HS256"


def create_access_token(data: dict, expires_minutes: int = 60):
    payload = data.copy()
    payload["exp"] = datetime.utcnow() + timedelta(minutes=expires_minutes)

    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)