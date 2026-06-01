"""
Regenerate embeddings for tourist areas using the proper embedding model
This script updates CARAGA_SEED_DATA.py with 384-dimensional embeddings
"""

import sys
import json
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app.services.ai.embedding_service import EmbeddingService
from CARAGA_SEED_DATA import CARAGA_TOURIST_AREAS

def regenerate_embeddings():
    """Generate proper 384-dimensional embeddings for all tourist areas"""
    
    print("🔄 Initializing embedding service...")
    embedding_service = EmbeddingService()
    print(f"✅ Using model: {embedding_service.model_name}")
    print(f"✅ Embedding dimension: {embedding_service.embedding_dim}")
    
    # Prepare content for each area
    contents = []
    for area in CARAGA_TOURIST_AREAS:
        # Create descriptive content for embedding
        content = f"{area['name']} {area['description']} {area['category']}"
        contents.append(content)
    
    print(f"\n🔄 Generating embeddings for {len(contents)} areas...")
    
    # Generate all embeddings at once
    embeddings = embedding_service.encode(contents)
    
    print(f"✅ Generated {len(embeddings)} embeddings")
    
    # Create updated vectors data
    vectors_data = []
    for i, (area, embedding) in enumerate(zip(CARAGA_TOURIST_AREAS, embeddings)):
        # Normalize embedding
        normalized_embedding = embedding_service.normalize_embedding(embedding)
        
        # Convert to JSON string for storage
        embedding_json = json.dumps(normalized_embedding.tolist())
        
        vectors_data.append({
            "vector_id": area["area_id"],
            "area_id": area["area_id"],
            "content": contents[i],
            "embedding": embedding_json,
        })
        
        print(f"  {i+1}. {area['name']}: {len(normalized_embedding)} dims")
    
    return vectors_data

def generate_python_code(vectors_data):
    """Generate Python code for CARAGA_SEED_DATA.py"""
    
    code = "TOURIST_AREA_VECTORS = [\n"
    
    for vector in vectors_data:
        code += f"""    {{
        "vector_id": {vector["vector_id"]},
        "area_id": {vector["area_id"]},
        "content": {repr(vector["content"])},
        "embedding": {repr(vector["embedding"])},
    }},
"""
    
    code += "]\n"
    return code

def main():
    """Main execution"""
    
    print("=" * 80)
    print("TOURIST AREA EMBEDDING REGENERATION SCRIPT")
    print("=" * 80)
    
    try:
        # Generate embeddings
        vectors_data = regenerate_embeddings()
        
        # Generate Python code
        print("\n📝 Generating Python code...")
        python_code = generate_python_code(vectors_data)
        
        # Read current CARAGA_SEED_DATA.py
        seed_file = project_root / "CARAGA_SEED_DATA.py"
        with open(seed_file, "r") as f:
            content = f.read()
        
        # Find and replace TOURIST_AREA_VECTORS section
        import re
        pattern = r"TOURIST_AREA_VECTORS = \[.*?\]"
        updated_content = re.sub(pattern, python_code.strip(), content, flags=re.DOTALL)
        
        # Backup original file
        backup_file = seed_file.with_suffix(".py.bak")
        with open(backup_file, "w") as f:
            f.write(content)
        print(f"💾 Backup created: {backup_file}")
        
        # Write updated file
        with open(seed_file, "w") as f:
            f.write(updated_content)
        
        print(f"✅ Updated: {seed_file}")
        
        print("\n" + "=" * 80)
        print("✨ REGENERATION COMPLETE!")
        print("=" * 80)
        print("\n📋 Next steps:")
        print("1. Run: python seed.py --table vectors --fresh")
        print("2. Test your AI endpoints again")
        print("3. The embeddings should now be 384-dimensional!")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
