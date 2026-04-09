from datetime import date
from uuid import UUID

from pydantic import BaseModel


class EquipmentTransactionBase(BaseModel):
    type: str
    quantity: int
    transaction_date: date
    remarks: str | None = None
    quipment_id: UUID


class EquipmentTransactionCreate(EquipmentTransactionBase):
    pass


class EquipmentTransactionUpdate(BaseModel):
    type: str | None = None
    quantity: int | None = None
    transaction_date: date | None = None
    remarks: str | None = None
    quipment_id: UUID | None = None


class EquipmentTransactionRead(EquipmentTransactionBase):
    equipment_trans_id: UUID

    class Config:
        from_attributes = True
