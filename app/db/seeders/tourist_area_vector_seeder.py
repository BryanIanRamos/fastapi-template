"""Tourist Area Vector seeder"""
import json
from app.db.seeders.base_seeder import BaseSeeder
from app.db.factories.factory import fake
from app.models.tourist_area_vector import TouristAreaVector
from app.models.tourist_area import TouristArea


class TouristAreaVectorSeeder(BaseSeeder):
    """Seed tourist_area_vectors table"""
    
    def run(self):
        """Create sample embeddings for tourist areas"""
        if self.count(TouristAreaVector) > 0:
            print("⏭️  Tourist area vectors table already seeded, skipping...")
            return
        
        areas = self.db.query(TouristArea).all()
        if not areas:
            print("⚠️  No tourist areas found. Seed tourist areas first.")
            return
        
        vectors = []
        
        # Example 1: One custom hardcoded vector
        vectors.append(TouristAreaVector(
            area_id=areas[0].area_id,
            content=areas[0].description,
            embedding=json.dumps([0.1] * 10),  # Mock embedding (10 dimensions)
        ))
        
        # Example 2: Generate 20 random vectors with Faker (change the range(20) to generate more)
        for _ in range(20):
            vectors.append(TouristAreaVector(
                area_id=fake.integer(min=areas[0].area_id, max=areas[-1].area_id),
                content=fake.paragraph(nb_sentences=3),
                embedding=json.dumps([float(fake.integer(min=0, max=100))/100 for _ in range(10)]),  # Mock embedding (10 dims)
            ))
        
        # TODO: Add more vectors here by adding more loops or custom entries above
        # Note: In production, use a real embedding model (OpenAI, Hugging Face, etc.)
        
        self.db.add_all(vectors)
        self.db.commit()
        print(f"✅ Seeded {len(vectors)} tourist area vectors")
