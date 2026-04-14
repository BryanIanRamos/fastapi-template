import uuid

from fastapi import APIRouter, Depends, Query, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.api.response import pagination_meta, success_response
from app.api.v1.endpoints.auth_system import get_current_system_user
from app.models.equipment_transactions import EquipmentTransaction
from app.models.users import SystemUser

router = APIRouter()


class EquipmentTransactionCreateRequest(BaseModel):
    model_config = ConfigDict(extra='forbid')
    
    equipmentId: uuid.UUID
    type: str
    quantityChange: int = 0
    date: str
    notes: str | None = None


@router.get("/")
def list_equipment_transactions(
    equipmentId: uuid.UUID | None = None,
    page: int = Query(default=1, ge=1),
    pageSize: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
    _: SystemUser = Depends(get_current_system_user),
):
    query = db.query(EquipmentTransaction)
    if equipmentId:
        query = query.filter(EquipmentTransaction.quipment_id == equipmentId)

    total = query.count()
    items = query.order_by(EquipmentTransaction.transaction_date.desc()).offset((page - 1) * pageSize).limit(pageSize).all()
    data = [
        {
            "id": str(item.equipment_trans_id),
            "equipmentId": str(item.quipment_id),
            "type": item.type,
            "quantity": item.quantity,
            "transactionDate": item.transaction_date.isoformat(),
            "remarks": item.remarks,
        }
        for item in items
    ]
    return success_response("OK", data, pagination_meta(page, pageSize, total))


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_equipment_transaction(
    payload: EquipmentTransactionCreateRequest,
    db: Session = Depends(get_db),
    _: SystemUser = Depends(get_current_system_user),
):
    from datetime import date

    row = EquipmentTransaction(
        quipment_id=payload.equipmentId,
        type=payload.type,
        quantity=payload.quantityChange,
        transaction_date=date.fromisoformat(payload.date),
        remarks=payload.notes,
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return success_response(
        "Created",
        {
            "id": str(row.equipment_trans_id),
            "equipmentId": str(row.quipment_id),
            "type": row.type,
            "quantity": row.quantity,
            "transactionDate": row.transaction_date.isoformat(),
            "remarks": row.remarks,
        },
    )
