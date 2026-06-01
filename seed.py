"""Seeder CLI - Similar to Laravel's php artisan db:seed"""
import sys
import argparse
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.db.seeders import (
    UserSeeder,
    TouristAreaSeeder,
    ActivitySeeder,
    ReviewSeeder,
    VisitSeeder,
    TaskSeeder,
    ProfileSeeder,
    TouristAreaVectorSeeder,
)
from app.models import Token, Session

# Mapping of table names to seeder classes
SEEDERS = {
    "users": UserSeeder,
    "profiles": ProfileSeeder,
    "tasks": TaskSeeder,
    "tourist_areas": TouristAreaSeeder,
    "activities": ActivitySeeder,
    "reviews": ReviewSeeder,
    "visits": VisitSeeder,
    "vectors": TouristAreaVectorSeeder,
}


def get_db() -> Session:
    """Get database session"""
    return SessionLocal()


def seed_table(db: Session, table_name: str):
    """Run seeder for a specific table"""
    if table_name not in SEEDERS:
        print(f"❌ Unknown table: {table_name}")
        print(f"Available tables: {', '.join(SEEDERS.keys())}")
        return False
    
    seeder_class = SEEDERS[table_name]
    seeder = seeder_class(db)
    seeder.run()
    return True


def seed_all(db: Session):
    """Seed all tables in order"""
    print("🌱 Seeding all tables...\n")
    order = ["users", "profiles", "tasks", "tourist_areas", "activities", "reviews", "visits", "vectors"]
    
    for table in order:
        seed_table(db, table)
        print()


def clear_table(db: Session, table_name: str):
    """Clear (truncate) a table"""
    from app.models import (
        User, TouristArea, AreaActivity, TouristReview, TouristVisit,
        Task, Profile, TouristAreaVector, Token, Session as SessionModel
    )
    
    model_map = {
        "users": User,
        "profiles": Profile,
        "tokens": Token,
        "sessions": SessionModel,
        "tasks": Task,
        "tourist_areas": TouristArea,
        "activities": AreaActivity,
        "reviews": TouristReview,
        "visits": TouristVisit,
        "vectors": TouristAreaVector,
    }
    
    if table_name not in model_map:
        print(f"❌ Unknown table: {table_name}")
        return False
    
    model = model_map[table_name]
    db.query(model).delete()
    db.commit()
    print(f"✅ Cleared {table_name} table")
    return True


def fresh_seed(db: Session, table_name: str):
    """Clear and reseed a specific table"""
    print(f"🔄 Clearing {table_name}...\n")
    clear_table(db, table_name)
    print(f"\n🌱 Reseeding {table_name}...\n")
    seed_table(db, table_name)


def reset_all(db: Session):
    """Clear ALL tables and reseed from scratch (like Laravel migrate:fresh --seed)"""
    print("🔄 Resetting database (deleting all data)...\n")
    # Order matters: clear in reverse order to respect foreign key constraints
    # Dependencies: sessions -> (tokens + users), tokens -> users, profiles -> users, tasks -> users
    clear_order = ["vectors", "visits", "reviews", "activities", "tourist_areas", "tasks", "sessions", "tokens", "profiles", "users"]
    seed_order = ["users", "profiles", "tokens", "sessions", "tasks", "tourist_areas", "activities", "reviews", "visits", "vectors"]
    
    # Clear all tables in reverse dependency order
    for table in clear_order:
        clear_table(db, table)
    
    print("\n🌱 Reseeding all tables...\n")
    for table in seed_order:
        seed_table(db, table)
        print()


def main():
    parser = argparse.ArgumentParser(description="Database Seeder (Laravel style)")
    parser.add_argument(
        "--table",
        type=str,
        help="Seed specific table",
        choices=list(SEEDERS.keys())
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Seed all tables"
    )
    parser.add_argument(
        "--fresh",
        action="store_true",
        help="Clear table before seeding (use with --table)"
    )
    parser.add_argument(
        "--reset",
        action="store_true",
        help="Clear ALL tables and reseed from scratch (like Laravel migrate:fresh --seed)"
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List available seeders"
    )
    
    args = parser.parse_args()
    
    # List available seeders
    if args.list:
        print("Available seeders:")
        for name in SEEDERS.keys():
            print(f"  - {name}")
        print("\nNote: tokens and sessions tables exist but are auto-managed (not manually seeded)")
        return
    
    db = get_db()
    
    try:
        if args.reset:
            reset_all(db)
        elif args.all:
            seed_all(db)
        elif args.table:
            if args.fresh:
                fresh_seed(db, args.table)
            else:
                seed_table(db, args.table)
        else:
            # Default: seed all if no arguments provided
            seed_all(db)
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        sys.exit(1)
    finally:
        db.close()


if __name__ == "__main__":
    main()
