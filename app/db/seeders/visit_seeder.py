"""Visit seeder for analytics"""
import sys
from pathlib import Path

from app.db.seeders.base_seeder import BaseSeeder
from app.models.tourist_visit import TouristVisit

# Add project root to path so we can import CARAGA_SEED_DATA
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))
from CARAGA_SEED_DATA import TOURIST_VISITS


class VisitSeeder(BaseSeeder):
    """Seed tourist_visits table for analytics with Caraga data"""
    
    def run(self):
        """Create sample visits from hardcoded data"""
        if self.count(TouristVisit) > 0:
            print("⏭️  Visits table already seeded, skipping...")
            return
        
        visits = []
        
        # Add all visits from hardcoded data
        # IMPORTANT: Use explicit IDs to match foreign key constraints
        for visit_data in TOURIST_VISITS:
            visits.append(TouristVisit(
                visit_id=visit_data["visit_id"],  # Explicitly set visit_id
                area_id=visit_data["area_id"],
                user_id=visit_data["user_id"],
                source=visit_data["source"],
                visit_time=visit_data["visit_time"],
            ))
        
        self.db.add_all(visits)
        self.db.commit()
        print(f"✅ Seeded {len(visits)} Caraga visits")
