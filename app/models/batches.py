from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.orm import relationship

from app.models.custom_base import SystemBase


class Batch(SystemBase):
    __tablename__ = "batch"

    batch_id = Column(String(50), primary_key=True)
    date_started = Column(Date, nullable=False)
    date_count = Column(Date, nullable=False)
    male_count = Column(Integer, nullable=False, default=0)
    female_count = Column(Integer, nullable=False, default=0)
    total_population = Column(Integer, nullable=False, default=0)
    status = Column(String(50), nullable=False)

    biological_assets = relationship("BiologicalAsset", back_populates="batch")
