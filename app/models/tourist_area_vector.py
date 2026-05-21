from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.db.base import Base


class TouristAreaVector(Base):
    """Tourist Area Vector model - Embeddings for semantic search"""
    __tablename__ = "tourist_area_vectors"

    vector_id = Column(Integer, primary_key=True, index=True)
    area_id = Column(Integer, ForeignKey("tourist_area.area_id", ondelete="CASCADE"), nullable=False, index=True)
    content = Column(Text, nullable=True)
    embedding = Column(String, nullable=True)  # Vector as string; use pgvector extension in DB
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationship
    area = relationship("TouristArea", back_populates="vectors")

    def __repr__(self):
        return f"<TouristAreaVector(vector_id={self.vector_id}, area_id={self.area_id})>"
