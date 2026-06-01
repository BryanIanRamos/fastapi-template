"""Tourist Area seeder"""
import sys
from pathlib import Path

from app.db.seeders.base_seeder import BaseSeeder
from app.models.tourist_area import TouristArea

# Add project root to path so we can import CARAGA_SEED_DATA
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))
from CARAGA_SEED_DATA import CARAGA_TOURIST_AREAS


class TouristAreaSeeder(BaseSeeder):
    """Seed tourist_area table with Caraga, PH tourist attractions"""
    
    def run(self):
        """Create sample tourist areas from hardcoded data"""
        if self.count(TouristArea) > 0:
            print("⏭️  Tourist areas table already seeded, skipping...")
            return
        
        areas = []
        
        # Add all Caraga tourist areas from hardcoded data
        # IMPORTANT: Set area_id explicitly to match AREA_ACTIVITIES foreign keys
        for area_data in CARAGA_TOURIST_AREAS:
            areas.append(TouristArea(
                area_id=area_data["area_id"],  # Explicitly set area_id
                name=area_data["name"],
                description=area_data["description"],
                location=area_data["location"],
                region=area_data["region"],
                latitude=area_data["latitude"],
                longitude=area_data["longitude"],
                category=area_data["category"],
            ))
        
        self.db.add_all(areas)
        self.db.commit()
        print(f"✅ Seeded {len(areas)} Caraga tourist areas")
