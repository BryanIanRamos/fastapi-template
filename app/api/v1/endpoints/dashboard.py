from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.api.response import success_response
from app.api.v1.endpoints.auth_system import get_current_system_user
from app.models.batches import Batch
from app.models.biological_assets import BiologicalAsset
from app.models.equipments import Equipment
from app.models.users import SystemUser

router = APIRouter()


@router.get("/summary")
def dashboard_summary(
    batchId: str | None = None,
    search: str | None = None,
    db: Session = Depends(get_db),
    _: SystemUser = Depends(get_current_system_user),
):
    bio_query = db.query(BiologicalAsset)
    if batchId:
        bio_query = bio_query.filter(BiologicalAsset.batch_id == batchId)
    if search:
        bio_query = bio_query.filter(BiologicalAsset.description.ilike(f"%{search}%"))

    equipment_total_value = db.query(func.coalesce(func.sum(Equipment.tiotal_value), 0)).scalar() or 0

    data = {
        "totalBatches": db.query(Batch).count(),
        "totalBiologicalAssets": bio_query.count(),
        "totalEquipments": db.query(Equipment).count(),
        "equipmentTotalValue": float(equipment_total_value),
    }
    return success_response("OK", data)
