"""Tourist Area seeder"""
from app.db.seeders.base_seeder import BaseSeeder
from app.db.factories.factory import fake
from app.models.tourist_area import TouristArea


class TouristAreaSeeder(BaseSeeder):
    """Seed tourist_area table"""
    
    def run(self):
        """Create sample tourist areas"""
        if self.count(TouristArea) > 0:
            print("⏭️  Tourist areas table already seeded, skipping...")
            return
        
        areas = []
        
        # Example 1: One custom hardcoded area
        areas.append(TouristArea(
            name="Eiffel Tower",
            description="The iconic iron lattice monument of Paris",
            location="Paris",
            region="Île-de-France",
            latitude=48.8584,
            longitude=2.2945,
            category="Monument",
        ))
        
        # Example 2: Generate 10 random tourist areas with Faker (change the range(10) to generate more)
        for _ in range(10):
            areas.append(TouristArea(
                name=fake.sentence(nb_words=4),
                description=fake.paragraph(nb_sentences=2),
                location=fake.city(),
                region=fake.state(),
                latitude=float(fake.latitude()),
                longitude=float(fake.longitude()),
                category=fake.word(),
            ))
        
        # TODO: Add more tourist areas here by adding more loops or custom entries above
        
        self.db.add_all(areas)
        self.db.commit()
        print(f"✅ Seeded {len(areas)} tourist areas")
