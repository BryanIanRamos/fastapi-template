from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.db.base import Base


class TouristVisit(Base):
    """Tourist Visits / Analytics model"""
    __tablename__ = "tourist_visits"

    visit_id = Column(Integer, primary_key=True, index=True)
    area_id = Column(Integer, ForeignKey("tourist_area.area_id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(Integer, nullable=True)
    source = Column(String, nullable=True)
    visit_time = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationship
    area = relationship("TouristArea", back_populates="visits")

    def __repr__(self):
        return f"<TouristVisit(visit_id={self.visit_id}, area_id={self.area_id}, user_id={self.user_id})>"
