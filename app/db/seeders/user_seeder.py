"""User seeder"""
from app.db.seeders.base_seeder import BaseSeeder
from app.db.factories.factory import fake
from app.models.user import User
from app.core.security import hash_password


class UserSeeder(BaseSeeder):
    """Seed users table"""
    
    def run(self):
        """Create sample users"""
        if self.count(User) > 0:
            print("⏭️  Users table already seeded, skipping...")
            return
        
        users = []
        
        # Example 1: One custom hardcoded user
        users.append(User(
            username="admin",
            email="admin@example.com",
            password=hash_password("admin123"),
            first_name="Admin",
            last_name="User",
            is_active=1,
            role=1,
        ))
        
        # Example 2: Generate 5 random users with Faker (change the range(5) to generate more)
        for _ in range(5):
            users.append(User(
                username=fake.username(),
                email=fake.email(),
                password=hash_password("password"),
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                is_active=1,
                role=2,
            ))
        
        # TODO: Add more users here by adding more loops or custom entries above
        
        self.db.add_all(users)
        self.db.commit()
        print(f"✅ Seeded {len(users)} users")
