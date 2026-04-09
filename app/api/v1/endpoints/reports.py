from fastapi import APIRouter, Depends, Query
from sqlalchemy import extract
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.api.response import success_response
from app.api.v1.endpoints.auth_system import get_current_system_user
from app.models.biological_assets import BiologicalAsset
from app.models.equipments import Equipment
from app.models.users import SystemUser

router = APIRouter()


def _filter_bio(query, month: int | None, year: int | None, batch_id: str | None):
    if month:
        query = query.filter(extract("month", BiologicalAsset.record_date) == month)
    if year:
        query = query.filter(extract("year", BiologicalAsset.record_date) == year)
    if batch_id:
        query = query.filter(BiologicalAsset.batch_id == batch_id)
    return query


@router.get("/biological-assets")
def report_biological_assets(
    month: int | None = Query(default=None, ge=1, le=12),
    year: int | None = None,
    batchId: str | None = None,
    db: Session = Depends(get_db),
    _: SystemUser = Depends(get_current_system_user),
):
    query = _filter_bio(db.query(BiologicalAsset), month, year, batchId)
    items = query.all()
    data = [{"id": item.bio_assets_id, "description": item.description, "recordDate": item.record_date.isoformat()} for item in items]
    return success_response("OK", data)


@router.get("/equipment")
def report_equipment(
    month: int | None = Query(default=None, ge=1, le=12),
    year: int | None = None,
    db: Session = Depends(get_db),
    _: SystemUser = Depends(get_current_system_user),
):
    query = db.query(Equipment)
    if month:
        query = query.filter(extract("month", Equipment.date_aquired) == month)
    if year:
        query = query.filter(extract("year", Equipment.date_aquired) == year)
    items = query.all()
    data = [{"id": str(item.equipment_id), "name": item.name, "status": item.status} for item in items]
    return success_response("OK", data)


@router.get("/mortality")
def report_mortality(
    month: int | None = Query(default=None, ge=1, le=12),
    year: int | None = None,
    batchId: str | None = None,
    db: Session = Depends(get_db),
    _: SystemUser = Depends(get_current_system_user),
):
    items = _filter_bio(db.query(BiologicalAsset), month, year, batchId).all()
    data = [{"id": item.bio_assets_id, "deathQty": item.death_qty, "deathFairVal": float(item.death_fair_val)} for item in items]
    return success_response("OK", data)


@router.get("/fair-value")
def report_fair_value(
    month: int | None = Query(default=None, ge=1, le=12),
    year: int | None = None,
    batchId: str | None = None,
    db: Session = Depends(get_db),
    _: SystemUser = Depends(get_current_system_user),
):
    items = _filter_bio(db.query(BiologicalAsset), month, year, batchId).all()
    data = [
        {
            "id": item.bio_assets_id,
            "beginFairVal": float(item.begin_fair_val),
            "additions": float(item.purchase_fair_val) + float(item.birth_fair_val) + float(item.add_change_fair_val),
            "deductions": float(item.sale_fair_val) + float(item.death_fair_val) + float(item.deduction_change_fair_value),
        }
        for item in items
    ]
    return success_response("OK", data)


@router.get("/rollforward")
def report_rollforward(
    year: int | None = None,
    db: Session = Depends(get_db),
    _: SystemUser = Depends(get_current_system_user),
):
    query = db.query(BiologicalAsset)
    if year:
        query = query.filter(extract("year", BiologicalAsset.record_date) == year)
    items = query.all()
    data = [{"id": item.bio_assets_id, "recordDate": item.record_date.isoformat(), "beginQty": item.begin_qty} for item in items]
    return success_response("OK", data)


@router.get("/export")
def export_report(
    type: str = "pdf",
    section: str | None = None,
    month: int | None = Query(default=None, ge=1, le=12),
    year: int | None = None,
    _: SystemUser = Depends(get_current_system_user),
):
    return success_response(
        "OK",
        {
            "type": type,
            "section": section,
            "month": month,
            "year": year,
            "downloadUrl": "/exports/mock-report.pdf",
        },
    )
