"""
Embedding Service - Handles vector embeddings for semantic search
Uses SentenceTransformer for generating embeddings
"""

import numpy as np
from typing import List, Optional
from sentence_transformers import SentenceTransformer


class EmbeddingService:
    """Service for generating and normalizing embeddings"""

    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        Initialize the embedding service
        
        Args:
            model_name: HuggingFace model name for embeddings
                       Default: all-MiniLM-L6-v2 (lightweight, fast)
                       Alternatives:
                       - all-mpnet-base-v2 (larger, more accurate)
                       - all-MiniLM-L12-v2 (medium, balanced)
        """
        self.model_name = model_name
        self.model = SentenceTransformer(model_name)
        self.embedding_dim = 384  # Default for all-MiniLM-L6-v2
        
        # Update dimension based on model
        if "mpnet" in model_name:
            self.embedding_dim = 768
        elif "L12" in model_name:
            self.embedding_dim = 384
        elif "L6" in model_name:
            self.embedding_dim = 384

    def encode(self, texts: List[str]) -> np.ndarray:
        """
        Encode texts to embeddings
        
        Args:
            texts: List of text strings to encode
            
        Returns:
            numpy array of embeddings
        """
        return self.model.encode(texts)

    def encode_single(self, text: str) -> np.ndarray:
        """
        Encode a single text to embedding
        
        Args:
            text: Text string to encode
            
        Returns:
            numpy array of embedding
        """
        return self.model.encode([text])[0]

    def normalize_embedding(self, vec: np.ndarray, target_dim: Optional[int] = None) -> np.ndarray:
        """
        Normalize embedding vector to target dimension
        
        Args:
            vec: Embedding vector
            target_dim: Target dimension (default: model's embedding_dim)
            
        Returns:
            Normalized embedding vector
        """
        if target_dim is None:
            target_dim = self.embedding_dim

        if len(vec) == target_dim:
            return vec

        if len(vec) > target_dim:
            # Truncate if too long
            return vec[:target_dim]

        # Pad with zeros if too short
        return np.pad(vec, (0, target_dim - len(vec)), mode="constant")

    def to_vector_literal(self, vec: np.ndarray) -> str:
        """
        Convert numpy vector to PostgreSQL pgvector literal format
        
        Args:
            vec: Embedding vector
            
        Returns:
            Vector literal string for pgvector: "[x1, x2, ..., xn]"
        """
        return "[" + ",".join(f"{x:.6f}" for x in vec) + "]"

    def to_vector_list(self, vec: np.ndarray) -> List[float]:
        """
        Convert numpy vector to Python list
        
        Args:
            vec: Embedding vector
            
        Returns:
            List of float values
        """
        return vec.tolist()

    def calculate_cosine_similarity(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        """
        Calculate cosine similarity between two vectors
        
        Args:
            vec1: First embedding vector
            vec2: Second embedding vector
            
        Returns:
            Cosine similarity score (0-1, where 1 is identical)
        """
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
            
        return float(np.dot(vec1, vec2) / (norm1 * norm2))

    def calculate_euclidean_distance(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        """
        Calculate Euclidean distance between two vectors
        
        Args:
            vec1: First embedding vector
            vec2: Second embedding vector
            
        Returns:
            Euclidean distance
        """
        return float(np.linalg.norm(vec1 - vec2))
