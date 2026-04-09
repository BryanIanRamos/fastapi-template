import uuid

from sqlalchemy import Column, Date, ForeignKey, Integer, String, Uuid
from sqlalchemy.orm import relationship

from app.models.custom_base import SystemBase


class EquipmentTransaction(SystemBase):
    __tablename__ = "equipment_transaction"

    equipment_trans_id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    type = Column(String(50), nullable=False)
    quantity = Column(Integer, nullable=False)
    transaction_date = Column(Date, nullable=False)
    remarks = Column(String(255), nullable=True)
    quipment_id = Column(Uuid, ForeignKey("equipments.equipment_id"), nullable=False, index=True)

    equipment = relationship("Equipment", back_populates="transactions")
