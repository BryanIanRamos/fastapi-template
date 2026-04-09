from sqlalchemy import DECIMAL, Column, Date, DateTime, ForeignKey, Integer, String, Uuid, func
from sqlalchemy.orm import relationship

from app.models.custom_base import SystemBase


class BiologicalAsset(SystemBase):
    __tablename__ = "biological_assets"

    bio_assets_id = Column(String(100), primary_key=True)
    description = Column(String(255), nullable=False)
    begin_qty = Column(Integer, nullable=False, default=0)
    begin_fair_val = Column(DECIMAL(14, 2), nullable=False, default=0)
    purchase_qty = Column(Integer, nullable=False, default=0)
    purchase_fair_val = Column(DECIMAL(14, 2), nullable=False, default=0)
    birth_qty = Column(Integer, nullable=False, default=0)
    birth_fair_val = Column(DECIMAL(14, 2), nullable=False, default=0)
    add_change_qty = Column(Integer, nullable=False, default=0)
    add_change_fair_val = Column(DECIMAL(14, 2), nullable=False, default=0)
    sale_qty = Column(Integer, nullable=False, default=0)
    sale_fair_val = Column(DECIMAL(14, 2), nullable=False, default=0)
    death_qty = Column(Integer, nullable=False, default=0)
    death_fair_val = Column(DECIMAL(14, 2), nullable=False, default=0)
    deduction_changes_qty = Column(Integer, nullable=False, default=0)
    deduction_change_fair_value = Column(DECIMAL(14, 2), nullable=False, default=0)
    remarks = Column(String(255), nullable=True)
    record_date = Column(Date, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    batch_id = Column(Uuid, ForeignKey("batch.batch_id"), nullable=False, index=True)

    batch = relationship("Batch", back_populates="biological_assets")
