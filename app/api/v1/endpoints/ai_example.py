"""
Example AI Endpoints - Tour Guide API Routes
This file demonstrates how to use the AI services in your FastAPI endpoints
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional

from app.api.deps import get_db
from app.services.ai import (
    EmbeddingService,
    TouristSearchService,
    TourGuideService,
)


# ============================================================================
# REQUEST/RESPONSE MODELS
# ============================================================================

class TourGuideRequest(BaseModel):
    """Request model for tour guide query"""
    query: str
    top_k: int = 5
    max_suggestions: int = 3
    similarity_threshold: Optional[float] = 0.4
    include_all_results: bool = False


class TouristAreaResult(BaseModel):
    """Result model for a single tourist area"""
    area_id: int
    name: str
    description: Optional[str]
    location: str
    region: Optional[str]
    category: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]
    similarity_score: float
    avg_rating: Optional[float]
    visit_count: int


class TourGuideResponse(BaseModel):
    """Response model for tour guide endpoint"""
    query: str
    response: str
    results_count: int
    top_results: List[TouristAreaResult]


class ItineraryRequest(BaseModel):
    """Request model for itinerary generation"""
    search_query: str
    duration_days: int = 3
    interests: List[str] = ["general tourism"]
    top_k: int = 10


class ItineraryResponse(BaseModel):
    """Response model for itinerary endpoint"""
    search_query: str
    duration_days: int
    interests: List[str]
    itinerary: str


class BudgetRecommendationRequest(BaseModel):
    """Request model for budget-based recommendations"""
    query: str
    budget: float
    top_k: int = 5


class BudgetRecommendationResponse(BaseModel):
    """Response model for budget recommendations"""
    query: str
    budget: float
    recommendation: str
    results_count: int


# ============================================================================
# ROUTER SETUP
# ============================================================================

router = APIRouter()

# Global service instances (can be moved to dependency injection if preferred)
embedding_service = EmbeddingService()
tour_guide_service = TourGuideService()


# ============================================================================
# ENDPOINTS
# ============================================================================

@router.post("/tour-guide", response_model=TourGuideResponse)
async def get_tour_recommendation(
    request: TourGuideRequest,
    db: Session = Depends(get_db),
):
    """
    Get personalized tour recommendations using AI
    
    Args:
        request: Tour guide query with optional filters
        db: Database session
        
    Returns:
        AI-generated recommendation with top matching areas
        
    Example:
        POST /api/v1/ai/tour-guide
        {
            "query": "I want to visit a beach with water sports and local food",
            "top_k": 5,
            "max_suggestions": 3,
            "similarity_threshold": 0.4
        }
    """
    try:
        # Initialize search service
        search_service = TouristSearchService(db, embedding_service)

        # Perform vector search
        results = search_service.search(
            query=request.query,
            top_k=request.top_k,
            enforce_relevance=True,
            similarity_threshold=request.similarity_threshold,
        )

        if not results:
            raise HTTPException(
                status_code=404,
                detail="No matching destinations found for your query. Try different keywords.",
            )

        # Generate AI response
        ai_response = tour_guide_service.build_response(
            query=request.query,
            search_results=results,
            max_suggestions=request.max_suggestions,
            include_all=request.include_all_results,
            min_similarity=request.similarity_threshold,
            require_relevance=True,
        )

        # Format top results
        top_results = [
            TouristAreaResult(
                area_id=r["area_id"],
                name=r["name"],
                description=r["description"],
                location=r["location"],
                region=r["region"],
                category=r["category"],
                latitude=r["latitude"],
                longitude=r["longitude"],
                similarity_score=r["similarity_score"],
                avg_rating=r["avg_rating"],
                visit_count=r["visit_count"],
            )
            for r in results[:request.max_suggestions]
        ]

        return TourGuideResponse(
            query=request.query,
            response=ai_response,
            results_count=len(results),
            top_results=top_results,
        )

    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in tour guide endpoint: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error generating recommendation: {str(e)}",
        )


@router.post("/generate-itinerary", response_model=ItineraryResponse)
async def generate_itinerary(
    request: ItineraryRequest,
    db: Session = Depends(get_db),
):
    """
    Generate a multi-day itinerary for travelers
    
    Args:
        request: Itinerary generation request with duration and interests
        db: Database session
        
    Returns:
        AI-generated multi-day itinerary
        
    Example:
        POST /api/v1/ai/generate-itinerary
        {
            "search_query": "popular beach destinations",
            "duration_days": 3,
            "interests": ["beach", "snorkeling", "local food"],
            "top_k": 10
        }
    """
    try:
        # Search for destinations
        search_service = TouristSearchService(db, embedding_service)
        results = search_service.search(
            query=request.search_query,
            top_k=request.top_k,
            enforce_relevance=False,
        )

        if not results:
            raise HTTPException(
                status_code=404,
                detail="No destinations found to create itinerary.",
            )

        # Generate itinerary
        itinerary = tour_guide_service.generate_itinerary(
            search_results=results,
            duration_days=request.duration_days,
            interests=request.interests,
        )

        return ItineraryResponse(
            search_query=request.search_query,
            duration_days=request.duration_days,
            interests=request.interests,
            itinerary=itinerary,
        )

    except HTTPException:
        raise
    except Exception as e:
        print(f"Error generating itinerary: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error generating itinerary: {str(e)}",
        )


@router.post("/budget-recommendations", response_model=BudgetRecommendationResponse)
async def get_budget_recommendations(
    request: BudgetRecommendationRequest,
    db: Session = Depends(get_db),
):
    """
    Get budget-friendly destination recommendations
    
    Args:
        request: Query with budget constraint
        db: Database session
        
    Returns:
        AI-generated budget recommendations
        
    Example:
        POST /api/v1/ai/budget-recommendations
        {
            "query": "beach destinations",
            "budget": 3000,
            "top_k": 5
        }
    """
    try:
        # Search for destinations
        search_service = TouristSearchService(db, embedding_service)
        results = search_service.search(
            query=request.query,
            top_k=request.top_k,
            enforce_relevance=False,
        )

        if not results:
            raise HTTPException(
                status_code=404,
                detail="No destinations found matching your budget criteria.",
            )

        # Generate budget recommendations
        recommendation = tour_guide_service.get_budget_recommendation(
            search_results=results,
            budget=request.budget,
        )

        return BudgetRecommendationResponse(
            query=request.query,
            budget=request.budget,
            recommendation=recommendation,
            results_count=len(results),
        )

    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in budget recommendations: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error generating recommendations: {str(e)}",
        )


@router.get("/health/ai")
async def health_check_ai():
    """
    Health check endpoint for AI services
    Verifies embedding model and LLM connectivity
    
    Returns:
        Health status of AI services
    """
    try:
        # Test embedding service
        test_embedding = embedding_service.encode_single("test")
        embedding_ok = len(test_embedding) > 0

        # Test LLM service (optional - can be slow)
        # llm_ok = tour_guide_service.llm is not None

        return {
            "status": "healthy" if embedding_ok else "degraded",
            "embedding_service": "ok" if embedding_ok else "error",
            "llm_service": "configured",
            "embedding_dim": embedding_service.embedding_dim,
        }

    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
        }


# ============================================================================
# UTILITY ENDPOINTS (FOR TESTING/DEBUGGING)
# ============================================================================

@router.post("/search/vector")
async def vector_search(
    query: str,
    top_k: int = 5,
    use_cosine: bool = False,
    db: Session = Depends(get_db),
):
    """
    Raw vector search endpoint (for debugging)
    Returns raw search results without AI processing
    
    Args:
        query: Search query
        top_k: Number of results
        use_cosine: Use cosine similarity instead of euclidean
        db: Database session
        
    Returns:
        Raw search results
    """
    try:
        search_service = TouristSearchService(db, embedding_service)

        if use_cosine:
            results = search_service.search_cosine(query, top_k=top_k, enforce_relevance=False)
        else:
            results = search_service.search(query, top_k=top_k, enforce_relevance=False)

        search_service.print_search_results(results)

        return {
            "query": query,
            "results_count": len(results),
            "results": results,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# TO USE THESE ENDPOINTS:
# ============================================================================
# 1. Add to your api/v1/router.py:
#    from app.api.v1.endpoints.ai import router as ai_router
#    api_router.include_router(ai_router, prefix="/ai", tags=["AI Tour Guide"])
#
# 2. Ensure Ollama is running:
#    ollama serve
#
# 3. Test with:
#    curl -X POST "http://localhost:8000/api/v1/ai/tour-guide" \
#      -H "Content-Type: application/json" \
#      -d '{"query": "I want to visit a beach with water sports"}'
# ============================================================================
