"""Activity seeder"""
import sys
from pathlib import Path

from app.db.seeders.base_seeder import BaseSeeder
from app.models.area_activity import AreaActivity

# Add project root to path so we can import CARAGA_SEED_DATA
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))
from CARAGA_SEED_DATA import AREA_ACTIVITIES


class ActivitySeeder(BaseSeeder):
    """Seed area_activities table with Caraga activities"""
    
    def run(self):
        """Create sample activities from hardcoded data"""
        if self.count(AreaActivity) > 0:
            print("⏭️  Activities table already seeded, skipping...")
            return
        
        activities = []
        
        # Add all activities from hardcoded data
        # IMPORTANT: Use explicit IDs to match foreign key constraints
        for activity_data in AREA_ACTIVITIES:
            activities.append(AreaActivity(
                activity_id=activity_data["activity_id"],  # Explicitly set activity_id
                area_id=activity_data["area_id"],
                activity_name=activity_data["activity_name"],
                description=activity_data["description"],
                difficulty_level=activity_data["difficulty_level"],
                estimated_duration=activity_data["estimated_duration"],
                price_range=activity_data["price_range"],
            ))
        
        self.db.add_all(activities)
        self.db.commit()
        print(f"✅ Seeded {len(activities)} Caraga activities")
