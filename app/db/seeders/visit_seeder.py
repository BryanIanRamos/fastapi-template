"""Visit seeder for analytics"""
from random import choice
from datetime import datetime, timedelta
from app.db.seeders.base_seeder import BaseSeeder
from app.db.factories.factory import fake
from app.models.tourist_visit import TouristVisit
from app.models.tourist_area import TouristArea


class VisitSeeder(BaseSeeder):
    """Seed tourist_visits table for analytics"""
    
    def run(self):
        """Create sample visits"""
        if self.count(TouristVisit) > 0:
            print("⏭️  Visits table already seeded, skipping...")
            return
        
        areas = self.db.query(TouristArea).all()
        if not areas:
            print("⚠️  No tourist areas found. Seed tourist areas first.")
            return
        
        sources = ["google", "tripadvisor", "instagram", "website", "friend_recommendation", "mobile_app"]
        visits = []
        
        # Example 1: One custom hardcoded visit
        visits.append(TouristVisit(
            area_id=areas[0].area_id,
            user_id=1,
            source="google",
            visit_time=datetime.now() - timedelta(days=5),
        ))
        
        # Example 2: Generate 50 random visits with Faker (change the range(50) to generate more)
        for _ in range(50):
            visits.append(TouristVisit(
                area_id=fake.integer(min=areas[0].area_id, max=areas[-1].area_id),
                user_id=fake.integer(min=1, max=100),
                source=choice(sources),
                visit_time=datetime.now() - timedelta(days=fake.integer(min=0, max=30)),
            ))
        
        # TODO: Add more visits here by adding more loops or custom entries above
        
        self.db.add_all(visits)
        self.db.commit()
        print(f"✅ Seeded {len(visits)} visits")
