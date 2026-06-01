# AI Tour Guide Service - Documentation

## Overview

The AI Tour Guide service provides intelligent tourist destination recommendations using vector embeddings and large language models (LLM). It combines semantic search with natural language generation to deliver personalized travel recommendations.

## Architecture

### Components

1. **EmbeddingService** - Generates and normalizes vector embeddings for text
2. **TouristSearchService** - Performs vector similarity search on tourist areas
3. **TourGuideService** - Generates natural language responses using LLM

### Data Flow

```
User Query
    ↓
EmbeddingService (Convert text to vector)
    ↓
TouristSearchService (Vector similarity search)
    ↓
Search Results (List of matching areas)
    ↓
TourGuideService (Generate AI response)
    ↓
Natural Language Recommendation
```

## Installation

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

Key packages:

- `sentence-transformers` - For embeddings
- `langchain` & `langchain-community` - For LLM integration
- `langchain-ollama` - For Ollama model support
- `numpy` - For vector operations

### 2. Setup Ollama (for LLM)

The system uses Ollama for running local LLMs. Install and setup:

```bash
# Download Ollama from https://ollama.ai
# Then pull a model
ollama pull gemma2
# or
ollama pull mistral
ollama pull neural-chat

# Start Ollama server (runs on http://localhost:11434 by default)
ollama serve
```

### 3. Database Setup

Ensure your database has the required tables:

- `tourist_area` - Main tourist destinations
- `tourist_area_vectors` - Embeddings for semantic search
- `area_activities` - Activities at each location
- `tourist_reviews` - User reviews and ratings
- `tourist_visits` - Visit history

## Usage

### Basic Example

```python
from sqlalchemy.orm import Session
from app.services.ai import (
    EmbeddingService,
    TouristSearchService,
    TourGuideService,
)
from app.db.session import SessionLocal

# Initialize services
db = SessionLocal()
embedding_service = EmbeddingService()
search_service = TouristSearchService(db, embedding_service)
guide_service = TourGuideService(llm_model="gemma2")

# User query
query = "I want to visit a beach with water activities and a 5k budget"

# Search for relevant destinations
results = search_service.search(
    query=query,
    top_k=5,
    enforce_relevance=True,
    similarity_threshold=0.3
)

# Generate AI response
response = guide_service.build_response(
    query=query,
    search_results=results,
    max_suggestions=3,
    min_similarity=0.4
)

print(response)

# Cleanup
db.close()
```

### Using in FastAPI Endpoint

```python
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.services.ai import TouristSearchService, TourGuideService
from pydantic import BaseModel

router = APIRouter()

class TourGuideQuery(BaseModel):
    query: str
    top_k: int = 5
    max_suggestions: int = 3

@router.post("/api/v1/ai/tour-guide")
async def get_tour_recommendation(
    request: TourGuideQuery,
    db: Session = Depends(get_db)
):
    search_service = TouristSearchService(db)
    guide_service = TourGuideService()

    # Search
    results = search_service.search(
        query=request.query,
        top_k=request.top_k
    )

    # Generate response
    response = guide_service.build_response(
        query=request.query,
        search_results=results,
        max_suggestions=request.max_suggestions
    )

    return {
        "query": request.query,
        "response": response,
        "results_count": len(results)
    }
```

## Service Details

### EmbeddingService

**Purpose**: Generate and manage text embeddings for semantic search

**Methods**:

- `encode(texts: List[str])` - Encode multiple texts
- `encode_single(text: str)` - Encode single text
- `normalize_embedding(vec, target_dim)` - Normalize to specific dimension
- `to_vector_literal(vec)` - Convert to PostgreSQL pgvector format
- `calculate_cosine_similarity(vec1, vec2)` - Cosine similarity
- `calculate_euclidean_distance(vec1, vec2)` - Euclidean distance

**Models Available**:

- `all-MiniLM-L6-v2` (default) - Fast, 384 dim (recommended for production)
- `all-mpnet-base-v2` - Accurate, 768 dim
- `all-MiniLM-L12-v2` - Medium, 384 dim

### TouristSearchService

**Purpose**: Perform vector similarity search on tourist areas

**Methods**:

- `search(query, top_k, enforce_relevance, similarity_threshold)` - Euclidean distance search
- `search_cosine(query, top_k, enforce_relevance, similarity_threshold)` - Cosine similarity search
- `is_tourist_query(query)` - Validate query is tourism-related
- `print_search_results(results)` - Format and print results

**Return Format**:

```python
{
    "area_id": int,
    "name": str,
    "description": str,
    "location": str,
    "region": str,
    "latitude": float,
    "longitude": float,
    "category": str,
    "similarity_score": float,  # 0-1
    "avg_rating": float,         # 1-5
    "visit_count": int,
    "activities": [{...}],
    "reviews": [{...}]
}
```

### TourGuideService

**Purpose**: Generate natural language responses using LLM

**Methods**:

- `build_response(query, search_results, max_suggestions, include_all, min_similarity, require_relevance)` - Generate recommendation
- `generate_itinerary(search_results, duration_days, interests)` - Create multi-day itinerary
- `get_budget_recommendation(search_results, budget)` - Budget-friendly recommendations

**LLM Configuration**:

- `llm_model`: Ollama model name (gemma2, mistral, neural-chat, etc.)
- `llm_temperature`: Response creativity (0-1, lower = more focused)
- `llm_base_url`: Ollama server URL

## Configuration

### Environment Variables

Add to `.env`:

```env
# Ollama Configuration
OLLAMA_MODEL=gemma2
OLLAMA_TEMPERATURE=0.2
OLLAMA_BASE_URL=http://localhost:11434

# Embedding Configuration
EMBEDDING_MODEL=all-MiniLM-L6-v2
```

### Database Vector Storage

**PostgreSQL with pgvector**:

```sql
-- Enable pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Update tourist_area_vectors table
ALTER TABLE tourist_area_vectors
ALTER COLUMN embedding TYPE vector(384) USING embedding::vector;
```

**SQLite**:

- Vectors stored as JSON string arrays
- Python-based similarity calculation
- Works for development, not recommended for production

## Advanced Usage

### Custom Similarity Threshold

```python
results = search_service.search(
    query="beach resort",
    top_k=10,
    similarity_threshold=0.5  # Only results > 50% match
)
```

### Itinerary Generation

```python
itinerary = guide_service.generate_itinerary(
    search_results=results,
    duration_days=5,
    interests=["adventure", "culture", "local food"]
)
```

### Budget Recommendations

```python
recommendation = guide_service.get_budget_recommendation(
    search_results=results,
    budget=5000
)
```

### Cosine vs Euclidean Similarity

```python
# Cosine Similarity (recommended for text embeddings)
results_cosine = search_service.search_cosine(
    query="mountain hiking",
    top_k=5
)

# Euclidean Distance (alternative)
results_euclidean = search_service.search(
    query="mountain hiking",
    top_k=5
)
```

## Performance Optimization

### 1. Vector Indexing (PostgreSQL)

```sql
-- Create HNSW index for faster similarity search
CREATE INDEX ON tourist_area_vectors USING hnsw (embedding vector_cosine_ops);
```

### 2. Caching Embeddings

Pre-compute and cache embeddings for tourist areas to avoid recalculation:

```python
# Generate embedding once during area creation
embedding = embedding_service.encode_single(area.description)
vector_literal = embedding_service.to_vector_literal(embedding)

# Save to database
new_vector = TouristAreaVector(
    area_id=area.area_id,
    content=area.description,
    embedding=vector_literal
)
```

### 3. Batch Processing

```python
# Encode multiple queries efficiently
queries = ["beach", "mountain", "city tour"]
embeddings = embedding_service.encode(queries)
```

## Troubleshooting

### Ollama Connection Error

**Error**: `HTTPConnectionError: Cannot connect to Ollama`

**Solution**:

1. Ensure Ollama is running: `ollama serve`
2. Check base URL matches environment
3. Verify port 11434 is accessible

### No Vector Results

**Causes**:

- No embeddings in `tourist_area_vectors` table
- Query not recognized as tourism-related (use `enforce_relevance=False`)
- Too high similarity threshold

**Solution**:

```python
results = search_service.search(
    query="beach",
    top_k=10,
    enforce_relevance=False,  # Disable relevance check
    similarity_threshold=0.0  # Accept all matches
)
```

### LLM Response Timeout

**Cause**: Model taking too long to generate response

**Solution**:

1. Use faster model: `gemma2` > `neural-chat` > `mistral`
2. Reduce context size: `max_suggestions=2`
3. Lower temperature for faster convergence

## Testing

### Unit Test Example

```python
def test_embedding_service():
    service = EmbeddingService()
    embedding = service.encode_single("beach resort")
    assert len(embedding) == 384
    assert all(isinstance(x, (int, float)) for x in embedding)

def test_vector_search():
    db = SessionLocal()
    search_service = TouristSearchService(db)
    results = search_service.search(
        query="mountain hiking",
        top_k=5,
        enforce_relevance=True
    )
    assert isinstance(results, list)
    db.close()
```

## API Endpoint Examples (To Implement)

### 1. Basic Tour Guide Query

```
POST /api/v1/ai/tour-guide
{
  "query": "I want a beach vacation with water sports",
  "top_k": 5,
  "max_suggestions": 3
}
```

### 2. Budget-Based Query

```
POST /api/v1/ai/budget-recommendations
{
  "query": "best destinations under 3000",
  "budget": 3000
}
```

### 3. Multi-Day Itinerary

```
POST /api/v1/ai/generate-itinerary
{
  "interests": ["adventure", "culture"],
  "duration_days": 5,
  "search_query": "popular destinations"
}
```

## Future Enhancements

1. **Multi-language support** - Translate queries and responses
2. **User preference learning** - Personalize based on history
3. **Real-time availability** - Integrate with booking systems
4. **Cost estimation** - Automatic budget calculation
5. **Route optimization** - Optimal travel routes between areas
6. **Image generation** - Create destination previews with image models
7. **Speech integration** - Voice-based queries and responses

## Security Considerations

1. **Input validation** - Sanitize user queries
2. **Rate limiting** - Prevent abuse of LLM API
3. **Sensitive data** - Don't log user queries with PII
4. **Model safety** - Use appropriate temperature to avoid harmful content
5. **API authentication** - Protect endpoints with auth middleware

## References

- [Sentence Transformers Documentation](https://www.sbert.net/)
- [LangChain Documentation](https://python.langchain.com/)
- [Ollama Documentation](https://ollama.ai/)
- [pgvector GitHub](https://github.com/pgvector/pgvector)
