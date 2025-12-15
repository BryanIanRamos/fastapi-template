"""Database initialization utilities"""
from sqlalchemy.orm import Session
from app.models.user import User
from app.core.security import hash_password


def init_db(db: Session) -> None:
    """Initialize database with sample data (optional)"""
    # Check if users table has data
    user_count = db.query(User).count()
    if user_count == 0:
        # Create sample user
        sample_user = User(
            email="admin@example.com",
            full_name="Admin User",
            hashed_password=hash_password("admin123"),
            is_active=1,
        )
        db.add(sample_user)
        db.commit()
        print("Sample user created: admin@example.com")
