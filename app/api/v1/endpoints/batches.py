import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.api.response import pagination_meta, success_response
from app.api.v1.endpoints.auth_system import get_current_system_user
from app.models.batches import Batch
from app.models.users import SystemUser

router = APIRouter()


class BatchCreateRequest(BaseModel):
    dateStarted: str
    dateCount: str
    maleCount: int = 0
    femaleCount: int = 0
    totalPopulation: int = 0
    status: str


class BatchUpdateRequest(BaseModel):
    dateStarted: str | None = None
    dateCount: str | None = None
    maleCount: int | None = None
    femaleCount: int | None = None
    totalPopulation: int | None = None
    status: str | None = None


@router.get("/")
def list_batches(
    status_filter: str | None = Query(default=None, alias="status"),
    page: int = Query(default=1, ge=1),
    pageSize: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
    _: SystemUser = Depends(get_current_system_user),
):
    query = db.query(Batch)
    if status_filter:
        query = query.filter(Batch.status == status_filter)

    total = query.count()
    items = query.order_by(Batch.date_started.desc()).offset((page - 1) * pageSize).limit(pageSize).all()
    data = [
        {
            "batchId": str(item.batch_id),
            "dateStarted": item.date_started.isoformat(),
            "dateCount": item.date_count.isoformat(),
            "maleCount": item.male_count,
            "femaleCount": item.female_count,
            "totalPopulation": item.total_population,
            "status": item.status,
        }
        for item in items
    ]
    return success_response("OK", data, pagination_meta(page, pageSize, total))


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_batch(payload: BatchCreateRequest, db: Session = Depends(get_db), _: SystemUser = Depends(get_current_system_user)):
    from datetime import date

    row = Batch(
        date_started=date.fromisoformat(payload.dateStarted),
        date_count=date.fromisoformat(payload.dateCount),
        male_count=payload.maleCount,
        female_count=payload.femaleCount,
        total_population=payload.totalPopulation,
        status=payload.status,
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return success_response(
        "Created",
        {
            "batchId": str(row.batch_id),
            "dateStarted": row.date_started.isoformat(),
            "dateCount": row.date_count.isoformat(),
            "maleCount": row.male_count,
            "femaleCount": row.female_count,
            "totalPopulation": row.total_population,
            "status": row.status,
        },
    )


@router.get("/{batch_id}")
def get_batch(batch_id: uuid.UUID, db: Session = Depends(get_db), _: SystemUser = Depends(get_current_system_user)):
    row = db.query(Batch).filter(Batch.batch_id == batch_id).first()
    if row is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Batch not found")
    return success_response(
        "OK",
        {
            "batchId": str(row.batch_id),
            "dateStarted": row.date_started.isoformat(),
            "dateCount": row.date_count.isoformat(),
            "maleCount": row.male_count,
            "femaleCount": row.female_count,
            "totalPopulation": row.total_population,
            "status": row.status,
        },
    )


@router.patch("/{batch_id}")
def update_batch(
    batch_id: uuid.UUID,
    payload: BatchUpdateRequest,
    db: Session = Depends(get_db),
    _: SystemUser = Depends(get_current_system_user),
):
    from datetime import date

    row = db.query(Batch).filter(Batch.batch_id == batch_id).first()
    if row is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Batch not found")

    if payload.dateStarted is not None:
        row.date_started = date.fromisoformat(payload.dateStarted)
    if payload.dateCount is not None:
        row.date_count = date.fromisoformat(payload.dateCount)
    if payload.maleCount is not None:
        row.male_count = payload.maleCount
    if payload.femaleCount is not None:
        row.female_count = payload.femaleCount
    if payload.totalPopulation is not None:
        row.total_population = payload.totalPopulation
    if payload.status is not None:
        row.status = payload.status

    db.add(row)
    db.commit()
    db.refresh(row)
    return success_response("Batch updated", {"batchId": str(row.batch_id)})


@router.delete("/{batch_id}")
def delete_batch(batch_id: uuid.UUID, db: Session = Depends(get_db), _: SystemUser = Depends(get_current_system_user)):
    row = db.query(Batch).filter(Batch.batch_id == batch_id).first()
    if row is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Batch not found")

    db.delete(row)
    db.commit()
    return success_response("Batch deleted", {"batchId": str(batch_id)})
