import uuid

from sqlalchemy import DECIMAL, Column, Date, Integer, String, Uuid
from sqlalchemy.orm import relationship

from app.models.custom_base import SystemBase


class Equipment(SystemBase):
    __tablename__ = "equipments"

    equipment_id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    name = Column(String(150), nullable=False)
    description = Column(String(255), nullable=True)
    quantity = Column(Integer, nullable=False, default=0)
    unit_value = Column(DECIMAL(14, 2), nullable=False, default=0)
    tiotal_value = Column(DECIMAL(14, 2), nullable=False, default=0)
    status = Column(String(50), nullable=False)
    date_aquired = Column(Date, nullable=True)
    remarks = Column(String(255), nullable=True)

    transactions = relationship("EquipmentTransaction", back_populates="equipment")
