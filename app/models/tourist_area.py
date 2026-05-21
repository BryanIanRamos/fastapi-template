from sqlalchemy import Column, Integer, String, Text, DateTime, Float, func
from sqlalchemy.orm import relationship
from app.db.base import Base


class TouristArea(Base):
    """Tourist Area model"""
    __tablename__ = "tourist_area"

    area_id = Column(Integer, primary_key=True, index=True)
    name = Column(Text, nullable=False)
    description = Column(Text, nullable=True)
    location = Column(Text, nullable=True)
    region = Column(Text, nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    category = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationships
    vectors = relationship("TouristAreaVector", back_populates="area", cascade="all, delete-orphan")
    activities = relationship("AreaActivity", back_populates="area", cascade="all, delete-orphan")
    reviews = relationship("TouristReview", back_populates="area", cascade="all, delete-orphan")
    visits = relationship("TouristVisit", back_populates="area", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<TouristArea(area_id={self.area_id}, name={self.name}, region={self.region})>"
