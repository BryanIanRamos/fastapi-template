"""Activity seeder"""
from app.db.seeders.base_seeder import BaseSeeder
from app.db.factories.factory import fake
from app.models.area_activity import AreaActivity
from app.models.tourist_area import TouristArea


class ActivitySeeder(BaseSeeder):
    """Seed area_activities table"""
    
    def run(self):
        """Create sample activities"""
        if self.count(AreaActivity) > 0:
            print("⏭️  Activities table already seeded, skipping...")
            return
        
        # Get all tourist areas
        areas = self.db.query(TouristArea).all()
        if not areas:
            print("⚠️  No tourist areas found. Seed tourist areas first.")
            return
        
        activities = []
        
        # Example 1: One custom hardcoded activity
        activities.append(AreaActivity(
            area_id=1,
            activity_name="Guided Tour",
            description="Professional guided tour of the Eiffel Tower",
            difficulty_level="Easy",
            estimated_duration="2 hours",
            price_range="$25-50",
        ))
        
        # Example 2: Generate 10 random activities with Faker (change the range(10) to generate more)
        for _ in range(10):
            activities.append(AreaActivity(
                area_id=fake.integer(min=1, max=len(areas)),
                activity_name=fake.words(nb=3),
                description=fake.paragraph(nb_sentences=2),
                difficulty_level=fake.word(),
                estimated_duration=f"{fake.integer(min=1, max=10)} hours",
                price_range=f"${fake.integer(min=10, max=500)}-{fake.integer(min=500, max=2000)}",
            ))
        
        # TODO: Add more activities here by adding more loops or custom entries above
        
        self.db.add_all(activities)
        self.db.commit()
        print(f"✅ Seeded {len(activities)} activities")
