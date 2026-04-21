import uuid

from sqlalchemy import Column, Date, ForeignKey, Integer, String, Uuid, func, select
from sqlalchemy.orm import relationship

from app.models.custom_base import SystemBase


def generate_equipment_trans_id(context):
    """Generate sequential equipment transaction ID like EQ-001, EQ-002, etc."""
    session = context.session
    last_record = session.query(EquipmentTransaction).order_by(
        EquipmentTransaction.equipment_trans_id.desc()
    ).first()
    
    if last_record and last_record.equipment_trans_id:
        # Extract number from ID like "EQ-001"
        try:
            num = int(last_record.equipment_trans_id.split('-')[1])
            return f"EQ-{num + 1:03d}"
        except (IndexError, ValueError):
            return "EQ-001"
    return "EQ-001"


class EquipmentTransaction(SystemBase):
    __tablename__ = "equipment_transaction"

    equipment_trans_id = Column(String(20), primary_key=True, default=generate_equipment_trans_id)
    type = Column(String(50), nullable=False)
    quantity = Column(Integer, nullable=False)
    transaction_date = Column(Date, nullable=False)
    remarks = Column(String(255), nullable=True)
    quipment_id = Column(Uuid, ForeignKey("equipments.equipment_id"), nullable=False, index=True)

    equipment = relationship("Equipment", back_populates="transactions")
