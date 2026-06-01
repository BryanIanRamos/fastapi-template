"""Tourist Area Vector seeder - Generates embeddings dynamically"""
import sys
import json
from pathlib import Path

from app.db.seeders.base_seeder import BaseSeeder
from app.models.tourist_area_vector import TouristAreaVector
from app.services.ai.embedding_service import EmbeddingService

# Add project root to path so we can import CARAGA_SEED_DATA
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))
from CARAGA_SEED_DATA import TOURIST_AREA_VECTORS


class TouristAreaVectorSeeder(BaseSeeder):
    """Seed tourist_area_vectors table with auto-generated embeddings"""
    
    def run(self):
        """Create embeddings for tourist areas on-the-fly during seeding"""
        if self.count(TouristAreaVector) > 0:
            print("⏭️  Tourist area vectors table already seeded, skipping...")
            return
        
        print("🔄 Initializing embedding service...")
        embedding_service = EmbeddingService()
        print(f"✅ Using model: {embedding_service.model_name}")
        print(f"✅ Embedding dimension: {embedding_service.embedding_dim}")
        
        # Extract content for all areas
        contents = [v["content"] for v in TOURIST_AREA_VECTORS]
        
        print(f"\n🔄 Generating embeddings for {len(contents)} areas...")
        
        # Generate all embeddings at once (efficient batch processing)
        embeddings = embedding_service.encode(contents)
        
        print(f"✅ Generated {len(embeddings)} embeddings\n")
        
        # Create vector records with generated embeddings
        vectors = []
        for idx, (vector_data, embedding) in enumerate(zip(TOURIST_AREA_VECTORS, embeddings)):
            # Normalize embedding to ensure consistent dimension
            normalized_embedding = embedding_service.normalize_embedding(embedding)
            
            # Convert to JSON string for storage
            embedding_json = json.dumps(normalized_embedding.tolist())
            
            area_id = vector_data["area_id"]
            content = vector_data["content"]
            
            vector = TouristAreaVector(
                area_id=area_id,
                content=content,
                embedding=embedding_json,  # Store as JSON string
            )
            vectors.append(vector)
            print(f"  {idx + 1}. Area {area_id}: {embedding_json[:50]}...")
        
        self.db.add_all(vectors)
        self.db.commit()
        print(f"\n✅ Seeded {len(vectors)} tourist area vectors with auto-generated embeddings")
