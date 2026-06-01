# Quick Start Guide - AI Tour Guide Integration

## ✅ What's Been Added

Your FastAPI application now has a complete AI-powered tour guide system integrated into `app/services/ai/`:

### 1. **Core Services**

- `embedding_service.py` - Vector embeddings using SentenceTransformer
- `tourist_search_service.py` - Vector similarity search for tourist areas
- `tour_guide_service.py` - LLM-based response generation

### 2. **API Examples**

- `app/api/v1/endpoints/ai_example.py` - Ready-to-use endpoint examples

### 3. **Documentation**

- `app/services/ai/tool_context.md` - Comprehensive guide

### 4. **Dependencies**

- Updated `requirements.txt` with required packages

## 🚀 Quick Setup

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Install and Run Ollama

```bash
# Download from https://ollama.ai
# Then run:
ollama serve

# In another terminal, pull a model:
ollama pull gemma2
```

### Step 3: Add Endpoints to Your Router

Edit `app/api/v1/router.py`:

```python
from app.api.v1.endpoints import ai_example

# Add this line with other router includes:
api_router.include_router(ai_example.router, prefix="/ai", tags=["AI Tour Guide"])
```

### Step 4: Test the Endpoints

```bash
# Start your FastAPI server
uvicorn app.main:app --reload

# In another terminal, test:
curl -X POST "http://localhost:8000/api/v1/ai/tour-guide" \
  -H "Content-Type: application/json" \
  -d '{"query": "I want a beach vacation with water sports"}'
```

## 📡 Available Endpoints (Once Integrated)

### 1. Tour Guide Recommendation

```
POST /api/v1/ai/tour-guide
```

Get personalized recommendations for tourist destinations

### 2. Generate Itinerary

```
POST /api/v1/ai/generate-itinerary
```

Create a multi-day travel itinerary

### 3. Budget Recommendations

```
POST /api/v1/ai/budget-recommendations
```

Get destinations within your budget

### 4. Vector Search (Debug)

```
POST /api/v1/ai/search/vector
```

Raw vector search results without AI processing

### 5. Health Check

```
GET /api/v1/ai/health/ai
```

Check AI services status

## 🎯 How It Works

1. **User submits query** → "I want a beach with water sports and local food"
2. **Embedding Service** → Converts query to vector
3. **Search Service** → Finds similar tourist areas using vector similarity
4. **Tour Guide Service** → Generates natural language response using LLM
5. **API returns** → Formatted recommendation with areas, activities, reviews, ratings

## 📊 Example Usage in Python

```python
from app.services.ai import (
    EmbeddingService,
    TouristSearchService,
    TourGuideService,
)
from app.db.session import SessionLocal

# Setup
db = SessionLocal()
embedding_service = EmbeddingService()
search_service = TouristSearchService(db, embedding_service)
guide_service = TourGuideService(llm_model="gemma2")

# Search
query = "beautiful beach with activities"
results = search_service.search(query, top_k=5)

# Generate response
response = guide_service.build_response(
    query=query,
    search_results=results,
    max_suggestions=3
)

print(response)
db.close()
```

## ⚙️ Configuration

Add these to your `.env` file for customization:

```env
# Ollama Configuration
OLLAMA_MODEL=gemma2
OLLAMA_TEMPERATURE=0.2
OLLAMA_BASE_URL=http://localhost:11434

# Embedding Configuration
EMBEDDING_MODEL=all-MiniLM-L6-v2
```

## 🔧 Troubleshooting

### "Cannot connect to Ollama"

- Ensure `ollama serve` is running
- Check that port 11434 is accessible
- Update `OLLAMA_BASE_URL` in `.env` if using different host

### "No vector results found"

- Ensure `tourist_area_vectors` table has embeddings
- Try with `enforce_relevance=False` in search
- Check similarity threshold isn't too high

### "LLM response too slow"

- Use `gemma2` (fastest) instead of larger models
- Reduce `max_suggestions` to lower context size
- Lower `temperature` for faster convergence

## 📦 File Structure

```
app/services/ai/
├── __init__.py                    # Module exports
├── embedding_service.py           # Vector embeddings
├── tourist_search_service.py      # Vector search
├── tour_guide_service.py          # LLM responses
└── tool_context.md               # Full documentation

app/api/v1/endpoints/
└── ai_example.py                 # Example endpoints (ready to use)
```

## 🎓 Next Steps

1. **Copy the example endpoints** to `app/api/v1/endpoints/ai.py`
2. **Integrate with your router** in `app/api/v1/router.py`
3. **Populate vector database** with embeddings for tourist areas
4. **Test through API** with different queries
5. **Customize responses** by modifying prompts in `tour_guide_service.py`

## 📚 Learn More

See `app/services/ai/tool_context.md` for:

- Detailed component documentation
- Advanced usage examples
- Performance optimization tips
- Database setup for PostgreSQL pgvector
- Security considerations
- Testing strategies

## ✨ Features

✅ Vector-based semantic search
✅ Multiple distance metrics (Euclidean, Cosine)
✅ LLM-powered natural language responses
✅ Budget-based recommendations
✅ Multi-day itinerary generation
✅ Activity and review aggregation
✅ Rating and popularity scoring
✅ Extensible and customizable
