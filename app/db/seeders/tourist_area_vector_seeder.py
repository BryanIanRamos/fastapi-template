"""Tourist Area Vector seeder"""
import sys
from pathlib import Path

from app.db.seeders.base_seeder import BaseSeeder
from app.models.tourist_area_vector import TouristAreaVector

# Add project root to path so we can import CARAGA_SEED_DATA
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))
from CARAGA_SEED_DATA import TOURIST_AREA_VECTORS


class TouristAreaVectorSeeder(BaseSeeder):
    """Seed tourist_area_vectors table with Caraga embeddings"""
    
    def run(self):
        """Create sample embeddings for tourist areas from hardcoded data"""
        if self.count(TouristAreaVector) > 0:
            print("⏭️  Tourist area vectors table already seeded, skipping...")
            return
        
        vectors = []
        
        # Add all vectors from hardcoded data
        # IMPORTANT: Use explicit IDs to match foreign key constraints
        for vector_data in TOURIST_AREA_VECTORS:
            vectors.append(TouristAreaVector(
                vector_id=vector_data["vector_id"],  # Explicitly set vector_id
                area_id=vector_data["area_id"],
                content=vector_data["content"],
                embedding=vector_data["embedding"],
            ))
        
        self.db.add_all(vectors)
        self.db.commit()
        print(f"✅ Seeded {len(vectors)} Caraga tourist area vectors")
