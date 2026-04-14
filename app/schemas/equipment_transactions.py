from datetime import date
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class EquipmentTransactionBase(BaseModel):
    type: str
    quantity: int
    transaction_date: date
    remarks: str | None = None
    quipment_id: UUID


class EquipmentTransactionCreate(EquipmentTransactionBase):
    model_config = ConfigDict(extra='forbid')


class EquipmentTransactionUpdate(BaseModel):
    model_config = ConfigDict(extra='forbid')
    
    type: str | None = None
    quantity: int | None = None
    transaction_date: date | None = None
    remarks: str | None = None
    quipment_id: UUID | None = None


class EquipmentTransactionRead(EquipmentTransactionBase):
    equipment_trans_id: UUID

    class Config:
        from_attributes = True
