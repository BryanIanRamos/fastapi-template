from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.db.base import Base


class AreaActivity(Base):
    """Area Activities model"""
    __tablename__ = "area_activities"

    activity_id = Column(Integer, primary_key=True, index=True)
    area_id = Column(Integer, ForeignKey("tourist_area.area_id", ondelete="CASCADE"), nullable=False, index=True)
    activity_name = Column(Text, nullable=True)
    description = Column(Text, nullable=True)
    difficulty_level = Column(Text, nullable=True)
    estimated_duration = Column(Text, nullable=True)
    price_range = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationship
    area = relationship("TouristArea", back_populates="activities")

    def __repr__(self):
        return f"<AreaActivity(activity_id={self.activity_id}, activity_name={self.activity_name})>"
