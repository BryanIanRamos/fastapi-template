"""Review seeder"""
import sys
from pathlib import Path

from app.db.seeders.base_seeder import BaseSeeder
from app.models.tourist_review import TouristReview

# Add project root to path so we can import CARAGA_SEED_DATA
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))
from CARAGA_SEED_DATA import TOURIST_REVIEWS


class ReviewSeeder(BaseSeeder):
    """Seed tourist_reviews table with Caraga reviews"""
    
    def run(self):
        """Create sample reviews from hardcoded data"""
        if self.count(TouristReview) > 0:
            print("⏭️  Reviews table already seeded, skipping...")
            return
        
        reviews = []
        
        # Add all reviews from hardcoded data
        # IMPORTANT: Use explicit IDs to match foreign key constraints
        for review_data in TOURIST_REVIEWS:
            reviews.append(TouristReview(
                review_id=review_data["review_id"],  # Explicitly set review_id
                area_id=review_data["area_id"],
                user_name=review_data["user_name"],
                rating=review_data["rating"],
                comment=review_data["comment"],
            ))
        
        self.db.add_all(reviews)
        self.db.commit()
        print(f"✅ Seeded {len(reviews)} Caraga reviews")
