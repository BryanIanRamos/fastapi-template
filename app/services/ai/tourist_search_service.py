"""
Tourist Search Service - Handles vector similarity search for tourist areas
Uses SQLAlchemy ORM for database queries
"""

import json
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func, text, and_
import numpy as np

from app.models.tourist_area import TouristArea
from app.models.tourist_area_vector import TouristAreaVector
from app.models.area_activity import AreaActivity
from app.models.tourist_review import TouristReview
from app.models.tourist_visit import TouristVisit
from app.services.ai.embedding_service import EmbeddingService


class TouristSearchService:
    """Service for vector-based search of tourist areas"""

    def __init__(self, db: Session, embedding_service: Optional[EmbeddingService] = None):
        """
        Initialize tourist search service
        
        Args:
            db: SQLAlchemy database session
            embedding_service: Embedding service instance (creates default if None)
        """
        self.db = db
        self.embedding_service = embedding_service or EmbeddingService()

    def is_tourist_query(self, query: str) -> bool:
        """
        Check if query is related to tourism
        
        Args:
            query: User query string
            
        Returns:
            True if query appears to be tourism-related
        """
        keywords = [
            "tourist", "tourism", "travel", "trip", "vacation", "itinerary",
            "visit", "destination", "spot", "place", "beach", "mountain",
            "island", "city", "museum", "park", "activity", "adventure",
            "food", "hotel", "hike", "hiking", "trail", "trek", "trekking",
            "resort", "attraction", "scenic", "tour", "explore", "sightseeing"
        ]
        query_lower = query.lower()
        return any(word in query_lower for word in keywords)

    def search(
        self,
        query: str,
        top_k: int = 5,
        enforce_relevance: bool = True,
        similarity_threshold: Optional[float] = None,
    ) -> List[Dict[str, Any]]:
        """
        Search for tourist areas using vector similarity (Euclidean distance)
        
        Args:
            query: User query string
            top_k: Number of top results to return
            enforce_relevance: Whether to check if query is tourism-related
            similarity_threshold: Minimum similarity score to include results
            
        Returns:
            List of matching tourist areas with related data
        """
        if enforce_relevance and not self.is_tourist_query(query):
            print("Query rejected: not related to tourist spots or activities.")
            return []

        # Generate embedding for query
        query_embedding = self.embedding_service.encode_single(query)
        query_embedding = self.embedding_service.normalize_embedding(query_embedding)

        try:
            # Query using SQLAlchemy - works with both PostgreSQL pgvector and SQLite
            # Note: For SQLite, this will use Python-based similarity calculation
            # For PostgreSQL with pgvector, you can optimize this query
            results = self._fetch_similar_areas(query_embedding, top_k, distance_metric="euclidean")
            
            # Filter by threshold if provided
            if similarity_threshold is not None:
                results = [r for r in results if r.get("similarity_score", 0) >= similarity_threshold]

            return results

        except Exception as e:
            print(f"Error during search: {e}")
            return []

    def search_cosine(
        self,
        query: str,
        top_k: int = 5,
        enforce_relevance: bool = True,
        similarity_threshold: Optional[float] = None,
    ) -> List[Dict[str, Any]]:
        """
        Search for tourist areas using cosine similarity
        
        Args:
            query: User query string
            top_k: Number of top results to return
            enforce_relevance: Whether to check if query is tourism-related
            similarity_threshold: Minimum similarity score to include results
            
        Returns:
            List of matching tourist areas with related data
        """
        if enforce_relevance and not self.is_tourist_query(query):
            print("Query rejected: not related to tourist spots or activities.")
            return []

        # Generate embedding for query
        query_embedding = self.embedding_service.encode_single(query)
        query_embedding = self.embedding_service.normalize_embedding(query_embedding)

        try:
            results = self._fetch_similar_areas(query_embedding, top_k, distance_metric="cosine")

            if similarity_threshold is not None:
                results = [r for r in results if r.get("similarity_score", 0) >= similarity_threshold]

            return results

        except Exception as e:
            print(f"Error during cosine search: {e}")
            return []

    def _fetch_similar_areas(
        self,
        query_embedding: np.ndarray,
        top_k: int,
        distance_metric: str = "euclidean",
    ) -> List[Dict[str, Any]]:
        """
        Fetch similar tourist areas using vector embeddings
        
        Args:
            query_embedding: Query embedding vector
            top_k: Number of results to return
            distance_metric: "euclidean" or "cosine"
            
        Returns:
            List of similar areas with metadata
        """
        # Get all tourist area vectors with their related data
        vectors = self.db.query(TouristAreaVector).all()

        if not vectors:
            return []

        # Detect stored embedding dimension from first vector
        stored_dim = None
        for vector in vectors:
            try:
                if isinstance(vector.embedding, str):
                    emb_list = json.loads(vector.embedding)
                    stored_dim = len(emb_list)
                else:
                    stored_dim = len(vector.embedding)
                break
            except:
                continue

        if stored_dim is None:
            print("Warning: Could not detect stored embedding dimension")
            return []

        # Adjust query embedding to match stored dimension
        if len(query_embedding) != stored_dim:
            if len(query_embedding) > stored_dim:
                # Truncate query embedding to match stored dimension
                adjusted_query = query_embedding[:stored_dim]
                print(f"Truncating query embedding from {len(query_embedding)} to {stored_dim} dims")
            else:
                # Pad query embedding with zeros
                adjusted_query = np.pad(query_embedding, (0, stored_dim - len(query_embedding)), mode="constant")
                print(f"Padding query embedding from {len(query_embedding)} to {stored_dim} dims")
        else:
            adjusted_query = query_embedding

        # Calculate similarity for each vector
        similarities = []
        for vector in vectors:
            try:
                # Parse embedding from storage
                if isinstance(vector.embedding, str):
                    # If stored as JSON array string
                    emb_list = json.loads(vector.embedding)
                    stored_embedding = np.array(emb_list)
                else:
                    stored_embedding = np.array(vector.embedding)

                # Ensure stored embedding matches expected dimension
                if len(stored_embedding) != stored_dim:
                    continue

                # Calculate distance using adjusted query embedding
                if distance_metric == "cosine":
                    similarity = self.embedding_service.calculate_cosine_similarity(
                        adjusted_query, stored_embedding
                    )
                else:  # euclidean
                    distance = self.embedding_service.calculate_euclidean_distance(
                        adjusted_query, stored_embedding
                    )
                    # Convert distance to similarity (inverse relationship)
                    # Normalize to 0-1 range (lower distance = higher similarity)
                    similarity = 1 / (1 + distance)

                similarities.append((vector, similarity))

            except Exception as e:
                print(f"Error processing vector {vector.vector_id}: {e}")
                continue

        # Sort by similarity (descending) and get top k
        similarities.sort(key=lambda x: x[1], reverse=True)
        top_vectors = similarities[:top_k]

        # Fetch complete data for top results
        results = []
        for vector, similarity_score in top_vectors:
            area = vector.area

            # Fetch related data
            activities = self.db.query(AreaActivity).filter(
                AreaActivity.area_id == area.area_id
            ).all()

            reviews = self.db.query(TouristReview).filter(
                TouristReview.area_id == area.area_id
            ).all()

            visits = self.db.query(TouristVisit).filter(
                TouristVisit.area_id == area.area_id
            ).all()

            # Calculate average rating
            avg_rating = self.db.query(func.avg(TouristReview.rating)).filter(
                TouristReview.area_id == area.area_id
            ).scalar()

            # Build result dictionary
            result = {
                "area_id": area.area_id,
                "name": area.name,
                "description": area.description,
                "location": area.location,
                "region": area.region,
                "latitude": area.latitude,
                "longitude": area.longitude,
                "category": area.category,
                "created_at": area.created_at.isoformat() if area.created_at else None,
                "vector_id": vector.vector_id,
                "content": vector.content,
                "vector_created_at": vector.created_at.isoformat() if vector.created_at else None,
                "similarity_score": float(similarity_score),
                "avg_rating": float(avg_rating) if avg_rating else None,
                "visit_count": len(visits),
                "activities": [
                    {
                        "activity_id": a.activity_id,
                        "area_id": a.area_id,
                        "activity_name": a.activity_name,
                        "description": a.description,
                        "difficulty_level": a.difficulty_level,
                        "estimated_duration": a.estimated_duration,
                        "price_range": a.price_range,
                        "created_at": a.created_at.isoformat() if a.created_at else None,
                    }
                    for a in activities
                ],
                "reviews": [
                    {
                        "review_id": r.review_id,
                        "user_name": r.user_name,
                        "rating": r.rating,
                        "comment": r.comment,
                        "created_at": r.created_at.isoformat() if r.created_at else None,
                    }
                    for r in reviews
                ],
            }

            results.append(result)

        return results

    def print_search_results(self, results: List[Dict[str, Any]]) -> None:
        """
        Print search results in a formatted way
        
        Args:
            results: List of search results
        """
        print("\n" + "=" * 80)
        print("SEARCH RESULTS")
        print("=" * 80)

        if not results:
            print("No results found.")
            return

        for i, result in enumerate(results, 1):
            name = result.get("name", "Unknown")
            location = result.get("location", "Unknown")
            similarity = result.get("similarity_score", 0)
            avg_rating = result.get("avg_rating", 0)
            visit_count = result.get("visit_count", 0)

            print(f"\n{i}. {name} in {location}")
            print(f"   Similarity Score: {similarity:.4f}")
            if avg_rating:
                print(f"   Average Rating: ⭐ {avg_rating:.1f}")
            print(f"   Visit Count: 👥 {visit_count}")

            desc = result.get("description", "")
            if desc:
                print(f"   Description: {desc[:100]}...")

            activities = result.get("activities", [])
            if activities:
                print(f"   Activities: {len(activities)} available")
                for act in activities[:2]:
                    print(f"     - {act.get('activity_name', 'Unknown')}")

            reviews = result.get("reviews", [])
            if reviews:
                print(f"   Recent Reviews: {len(reviews)} total")
                for rev in reviews[:1]:
                    print(f"     - {rev.get('user_name', 'Anonymous')}: ⭐ {rev.get('rating')} - {rev.get('comment', '')[:60]}")

        print("\n" + "=" * 80)
