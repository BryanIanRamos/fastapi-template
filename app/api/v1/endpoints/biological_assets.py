import random
import string

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.api.deps import get_db
from app.api.response import pagination_meta, success_response
from app.api.v1.endpoints.auth_system import get_current_system_user
from app.models.biological_assets import BiologicalAsset
from app.models.users import SystemUser

router = APIRouter()


class BiologicalAssetCreateRequest(BaseModel):
    model_config = ConfigDict(extra='forbid')
    
    bioAssetsId: str | None = None
    description: str
    beginQty: int = 0
    beginFairVal: float = 0
    purchaseQty: int = 0
    purchaseFairVal: float = 0
    birthQty: int = 0
    birthFairVal: float = 0
    addChangeQty: int = 0
    addChangeFairVal: float = 0
    saleQty: int = 0
    saleFairVal: float = 0
    deathQty: int = 0
    deathFairVal: float = 0
    deductionChangesQty: int = 0
    deductionChangeFairValue: float = 0
    remarks: str | None = None
    recordDate: str
    batchId: str

model_config = ConfigDict(extra='forbid')
    
    
class BiologicalAssetUpdateRequest(BaseModel):
    description: str | None = None
    remarks: str | None = None


def _to_payload(item: BiologicalAsset) -> dict:
    return {
        "id": item.bio_assets_id,
        "description": item.description,
        "beginQty": item.begin_qty,
        "beginFairVal": float(item.begin_fair_val),
        "purchaseQty": item.purchase_qty,
        "purchaseFairVal": float(item.purchase_fair_val),
        "birthQty": item.birth_qty,
        "birthFairVal": float(item.birth_fair_val),
        "addChangeQty": item.add_change_qty,
        "addChangeFairVal": float(item.add_change_fair_val),
        "saleQty": item.sale_qty,
        "saleFairVal": float(item.sale_fair_val),
        "deathQty": item.death_qty,
        "deathFairVal": float(item.death_fair_val),
        "deductionChangesQty": item.deduction_changes_qty,
        "deductionChangeFairValue": float(item.deduction_change_fair_value),
        "remarks": item.remarks,
        "recordDate": item.record_date.isoformat(),
        "createdAt": item.created_at.isoformat() if item.created_at else None,
        "updatedAt": item.updated_at.isoformat() if item.updated_at else None,
        "batchId": str(item.batch_id),
    }


@router.get("/")
def list_biological_assets(
    page: int = Query(default=1, ge=1),
    pageSize: int = Query(default=20, ge=1, le=100),
    search: str | None = None,
    batchId: str | None = None,
    db: Session = Depends(get_db),
    _: SystemUser = Depends(get_current_system_user),
):
    query = db.query(BiologicalAsset)
    if search:
        query = query.filter(BiologicalAsset.description.ilike(f"%{search}%"))
    if batchId:
        query = query.filter(BiologicalAsset.batch_id == batchId)

    total = query.count()
    items = query.order_by(BiologicalAsset.record_date.desc()).offset((page - 1) * pageSize).limit(pageSize).all()
    return success_response("OK", [_to_payload(item) for item in items], pagination_meta(page, pageSize, total))


def _generate_unique_bio_id(db: Session, max_attempts: int = 10) -> str:
    """Generate a unique biological asset ID"""
    for _ in range(max_attempts):
        suffix = "".join(random.choice(string.digits) for _ in range(6))
        bio_id = f"BIO-{suffix}"
        # Check if ID already exists
        if not db.query(BiologicalAsset).filter(BiologicalAsset.bio_assets_id == bio_id).first():
            return bio_id
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to generate unique ID after multiple attempts")


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_biological_asset(
    payload: BiologicalAssetCreateRequest,
    db: Session = Depends(get_db),
    _: SystemUser = Depends(get_current_system_user),
):
    from datetime import date

    # Auto-generate bioAssetsId if not provided
    bio_assets_id = payload.bioAssetsId
    if not bio_assets_id:
        bio_assets_id = _generate_unique_bio_id(db)
    else:
        # Check if provided ID already exists
        existing = db.query(BiologicalAsset).filter(BiologicalAsset.bio_assets_id == bio_assets_id).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Biological asset with ID '{bio_assets_id}' already exists"
            )

    try:
        row = BiologicalAsset(
            bio_assets_id=bio_assets_id,
            description=payload.description,
            begin_qty=payload.beginQty,
            begin_fair_val=payload.beginFairVal,
            purchase_qty=payload.purchaseQty,
            purchase_fair_val=payload.purchaseFairVal,
            birth_qty=payload.birthQty,
            birth_fair_val=payload.birthFairVal,
            add_change_qty=payload.addChangeQty,
            add_change_fair_val=payload.addChangeFairVal,
            sale_qty=payload.saleQty,
            sale_fair_val=payload.saleFairVal,
            death_qty=payload.deathQty,
            death_fair_val=payload.deathFairVal,
            deduction_changes_qty=payload.deductionChangesQty,
            deduction_change_fair_value=payload.deductionChangeFairValue,
            remarks=payload.remarks,
            record_date=date.fromisoformat(payload.recordDate),
            batch_id=payload.batchId,
        )
        db.add(row)
        db.commit()
        db.refresh(row)
        return success_response("Created", _to_payload(row))
    except IntegrityError as e:
        db.rollback()
        # Handle foreign key violation (batch_id doesn't exist)
        if "batch" in str(e.orig).lower():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid batch ID. The specified batch does not exist"
            )
        # Handle any other integrity constraint violations
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to create biological asset due to constraint violation"
        )


@router.get("/generate-number")
def generate_bio_number(_: SystemUser = Depends(get_current_system_user)):
    suffix = "".join(random.choice(string.digits) for _ in range(6))
    return success_response("OK", {"id": f"BIO-{suffix}"})


@router.get("/{bio_id}")
def get_biological_asset(bio_id: str, db: Session = Depends(get_db), _: SystemUser = Depends(get_current_system_user)):
    row = db.query(BiologicalAsset).filter(BiologicalAsset.bio_assets_id == bio_id).first()
    if row is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Biological asset not found")
    return success_response("OK", _to_payload(row))


@router.patch("/{bio_id}")
def update_biological_asset(
    bio_id: str,
    payload: BiologicalAssetUpdateRequest,
    db: Session = Depends(get_db),
    _: SystemUser = Depends(get_current_system_user),
):
    row = db.query(BiologicalAsset).filter(BiologicalAsset.bio_assets_id == bio_id).first()
    if row is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Biological asset not found")

    if payload.description is not None:
        row.description = payload.description
    if payload.remarks is not None:
        row.remarks = payload.remarks

    db.add(row)
    db.commit()
    db.refresh(row)
    return success_response("Updated", _to_payload(row))


@router.delete("/{bio_id}")
def delete_biological_asset(bio_id: str, db: Session = Depends(get_db), _: SystemUser = Depends(get_current_system_user)):
    row = db.query(BiologicalAsset).filter(BiologicalAsset.bio_assets_id == bio_id).first()
    if row is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Biological asset not found")

    db.delete(row)
    db.commit()
    return success_response("Deleted", {"id": bio_id})
