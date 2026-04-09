import uuid

from sqlalchemy import Column, Date, Integer, String, Uuid
from sqlalchemy.orm import relationship

from app.models.custom_base import SystemBase


class Batch(SystemBase):
    __tablename__ = "batch"

    batch_id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    date_started = Column(Date, nullable=False)
    date_count = Column(Date, nullable=False)
    male_count = Column(Integer, nullable=False, default=0)
    female_count = Column(Integer, nullable=False, default=0)
    total_population = Column(Integer, nullable=False, default=0)
    status = Column(String(50), nullable=False)

    biological_assets = relationship("BiologicalAsset", back_populates="batch")
