import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.api.response import pagination_meta, success_response
from app.api.v1.endpoints.auth_system import get_current_system_user
from app.models.equipments import Equipment
from app.models.users import SystemUser

router = APIRouter()


class EquipmentCreateRequest(BaseModel):
    model_config = ConfigDict(extra='forbid')
    
    name: str
    description: str | None = None
    quantity: int = 0
    unitValue: float = 0
    tiotalValue: float = 0
    status: str
    dateAquired: str | None = None
    remarks: str | None = None


class EquipmentUpdateRequest(BaseModel):
    model_config = ConfigDict(extra='forbid')
    
    name: str | None = None
    description: str | None = None
    quantity: int | None = None
    unitValue: float | None = None
    tiotalValue: float | None = None
    status: str | None = None
    dateAquired: str | None = None
    remarks: str | None = None


def _to_payload(item: Equipment) -> dict:
    return {
        "id": str(item.equipment_id),
        "name": item.name,
        "description": item.description,
        "quantity": item.quantity,
        "unitValue": float(item.unit_value),
        "tiotalValue": float(item.tiotal_value),
        "status": item.status,
        "dateAquired": item.date_aquired.isoformat() if item.date_aquired else None,
        "remarks": item.remarks,
    }


@router.get("/")
def list_equipments(
    page: int = Query(default=1, ge=1),
    pageSize: int = Query(default=20, ge=1, le=100),
    search: str | None = None,
    status_filter: str | None = Query(default=None, alias="status"),
    db: Session = Depends(get_db),
    _: SystemUser = Depends(get_current_system_user),
):
    query = db.query(Equipment)
    if search:
        query = query.filter(Equipment.name.ilike(f"%{search}%"))
    if status_filter:
        query = query.filter(Equipment.status == status_filter)

    total = query.count()
    items = query.order_by(Equipment.name.asc()).offset((page - 1) * pageSize).limit(pageSize).all()
    return success_response("OK", [_to_payload(item) for item in items], pagination_meta(page, pageSize, total))


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_equipment(payload: EquipmentCreateRequest, db: Session = Depends(get_db), _: SystemUser = Depends(get_current_system_user)):
    from datetime import date

    row = Equipment(
        name=payload.name,
        description=payload.description,
        quantity=payload.quantity,
        unit_value=payload.unitValue,
        tiotal_value=payload.tiotalValue,
        status=payload.status,
        date_aquired=date.fromisoformat(payload.dateAquired) if payload.dateAquired else None,
        remarks=payload.remarks,
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return success_response("Created", _to_payload(row))


@router.get("/{equipment_id}")
def get_equipment(equipment_id: uuid.UUID, db: Session = Depends(get_db), _: SystemUser = Depends(get_current_system_user)):
    row = db.query(Equipment).filter(Equipment.equipment_id == equipment_id).first()
    if row is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Equipment not found")
    return success_response("OK", _to_payload(row))


@router.patch("/{equipment_id}")
def update_equipment(
    equipment_id: uuid.UUID,
    payload: EquipmentUpdateRequest,
    db: Session = Depends(get_db),
    _: SystemUser = Depends(get_current_system_user),
):
    from datetime import date

    row = db.query(Equipment).filter(Equipment.equipment_id == equipment_id).first()
    if row is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Equipment not found")

    if payload.name is not None:
        row.name = payload.name
    if payload.description is not None:
        row.description = payload.description
    if payload.quantity is not None:
        row.quantity = payload.quantity
    if payload.unitValue is not None:
        row.unit_value = payload.unitValue
    if payload.tiotalValue is not None:
        row.tiotal_value = payload.tiotalValue
    if payload.status is not None:
        row.status = payload.status
    if payload.dateAquired is not None:
        row.date_aquired = date.fromisoformat(payload.dateAquired)
    if payload.remarks is not None:
        row.remarks = payload.remarks

    db.add(row)
    db.commit()
    db.refresh(row)
    return success_response("Updated", _to_payload(row))


@router.delete("/{equipment_id}")
def delete_equipment(equipment_id: uuid.UUID, db: Session = Depends(get_db), _: SystemUser = Depends(get_current_system_user)):
    row = db.query(Equipment).filter(Equipment.equipment_id == equipment_id).first()
    if row is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Equipment not found")

    db.delete(row)
    db.commit()
    return success_response("Deleted", {"id": str(equipment_id)})
