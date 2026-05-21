from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, CheckConstraint, func
from sqlalchemy.orm import relationship
from app.db.base import Base


class TouristReview(Base):
    """Tourist Reviews model"""
    __tablename__ = "tourist_reviews"
    __table_args__ = (
        CheckConstraint("rating >= 1 AND rating <= 5", name="ck_rating_range"),
    )

    review_id = Column(Integer, primary_key=True, index=True)
    area_id = Column(Integer, ForeignKey("tourist_area.area_id", ondelete="CASCADE"), nullable=False, index=True)
    user_name = Column(Text, nullable=True)
    rating = Column(Integer, nullable=False)
    comment = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationship
    area = relationship("TouristArea", back_populates="reviews")

    def __repr__(self):
        return f"<TouristReview(review_id={self.review_id}, area_id={self.area_id}, rating={self.rating})>"
