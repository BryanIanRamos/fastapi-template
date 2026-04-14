from datetime import date, datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class BiologicalAssetBase(BaseModel):
    description: str
    begin_qty: int = 0
    begin_fair_val: Decimal = Decimal("0")
    purchase_qty: int = 0
    purchase_fair_val: Decimal = Decimal("0")
    birth_qty: int = 0
    birth_fair_val: Decimal = Decimal("0")
    add_change_qty: int = 0
    add_change_fair_val: Decimal = Decimal("0")
    sale_qty: int = 0
    sale_fair_val: Decimal = Decimal("0")
    death_qty: int = 0
    death_fair_val: Decimal = Decimal("0")
    deduction_changes_qty: int = 0
    deduction_change_fair_value: Decimal = Decimal("0")
    remarks: str | None = None
    record_date: date
    batch_id: UUID


class BiologicalAssetCreate(BiologicalAssetBase):
    model_config = ConfigDict(extra='forbid')
    
    bio_assets_id: str


class BiologicalAssetUpdate(BaseModel):
    model_config = ConfigDict(extra='forbid')
    
    description: str | None = None
    begin_qty: int | None = None
    begin_fair_val: Decimal | None = None
    purchase_qty: int | None = None
    purchase_fair_val: Decimal | None = None
    birth_qty: int | None = None
    birth_fair_val: Decimal | None = None
    add_change_qty: int | None = None
    add_change_fair_val: Decimal | None = None
    sale_qty: int | None = None
    sale_fair_val: Decimal | None = None
    death_qty: int | None = None
    death_fair_val: Decimal | None = None
    deduction_changes_qty: int | None = None
    deduction_change_fair_value: Decimal | None = None
    remarks: str | None = None
    record_date: date | None = None
    batch_id: UUID | None = None


class BiologicalAssetRead(BiologicalAssetBase):
    bio_assets_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
