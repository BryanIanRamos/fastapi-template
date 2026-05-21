"""Profile seeder"""
from app.db.seeders.base_seeder import BaseSeeder
from app.db.factories.factory import fake
from app.models.profile import Profile
from app.models.user import User


class ProfileSeeder(BaseSeeder):
    """Seed profiles table"""
    
    def run(self):
        """Create sample profiles"""
        if self.count(Profile) > 0:
            print("⏭️  Profiles table already seeded, skipping...")
            return
        
        users = self.db.query(User).all()
        if not users:
            print("⚠️  No users found. Seed users first.")
            return
        
        genders = ["Male", "Female", "Other"]
        profiles = []
        
        # Example 1: One custom hardcoded profile
        profiles.append(Profile(
            user_id=users[0].user_id,
            first_name="Admin",
            last_name="User",
            phone_number="+1-555-0100",
            birthday="1990-01-01",
            gender="Other",
            profile_picture_url="https://example.com/admin.jpg",
        ))
        
        # Example 2: Generate 10 random profiles with Faker (change the range(10) to generate more)
        for user in users[1:]:
            profiles.append(Profile(
                user_id=user.user_id,
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                phone_number=fake.phone_number(),
                birthday=fake.date(),
                gender=fake.word() if fake.word() in genders else "Other",
                profile_picture_url=fake.url(),
            ))
        
        # TODO: Add more profiles here by adding more loops or custom entries above
        
        self.db.add_all(profiles)
        self.db.commit()
        print(f"✅ Seeded {len(profiles)} profiles")
