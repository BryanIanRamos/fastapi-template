from datetime import date
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel


class EquipmentBase(BaseModel):
    name: str
    description: str | None = None
    quantity: int = 0
    unit_value: Decimal = Decimal("0")
    tiotal_value: Decimal = Decimal("0")
    status: str
    date_aquired: date | None = None
    remarks: str | None = None


class EquipmentCreate(EquipmentBase):
    pass


class EquipmentUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    quantity: int | None = None
    unit_value: Decimal | None = None
    tiotal_value: Decimal | None = None
    status: str | None = None
    date_aquired: date | None = None
    remarks: str | None = None


class EquipmentRead(EquipmentBase):
    equipment_id: UUID

    class Config:
        from_attributes = True
