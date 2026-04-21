"""Database initialization utilities"""
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.users import SystemUser
from app.core.security import hash_password


def init_db(db: Session) -> None:
    """Initialize database with sample data (optional)"""
    # Check if users table has data
    user_count = db.query(SystemUser).count()
    if user_count == 0:
        # Create sample system admin user
        sample_user = SystemUser(
            email="admin@example.com",
            password=hash_password("admin123"),
            role=1,
        )
        db.add(sample_user)
        db.commit()
        print("Sample admin user created: admin@example.com")


def run_seed() -> None:
    """Run the database seeder with an internally managed DB session."""
    db = SessionLocal()
    try:
        init_db(db)
    finally:
        db.close()


if __name__ == "__main__":
    run_seed()
