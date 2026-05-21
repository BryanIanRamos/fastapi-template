"""Review seeder"""
from app.db.seeders.base_seeder import BaseSeeder
from app.db.factories.factory import fake
from app.models.tourist_review import TouristReview
from app.models.tourist_area import TouristArea


class ReviewSeeder(BaseSeeder):
    """Seed tourist_reviews table"""
    
    def run(self):
        """Create sample reviews"""
        if self.count(TouristReview) > 0:
            print("⏭️  Reviews table already seeded, skipping...")
            return
        
        areas = self.db.query(TouristArea).all()
        if not areas:
            print("⚠️  No tourist areas found. Seed tourist areas first.")
            return
        
        reviews = []
        
        # Example 1: One custom hardcoded review
        reviews.append(TouristReview(
            area_id=areas[0].area_id,
            user_name="John Smith",
            rating=5,
            comment="Amazing experience! Highly recommended.",
        ))
        
        # Example 2: Generate 20 random reviews with Faker (change the range(20) to generate more)
        for _ in range(20):
            reviews.append(TouristReview(
                area_id=fake.integer(min=areas[0].area_id, max=areas[-1].area_id),
                user_name=fake.name(),
                rating=fake.rating(min=3, max=5),
                comment=fake.paragraph(nb_sentences=2),
            ))
        
        # TODO: Add more reviews here by adding more loops or custom entries above
        
        self.db.add_all(reviews)
        self.db.commit()
        print(f"✅ Seeded {len(reviews)} reviews")
