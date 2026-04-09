import uuid

from fastapi import APIRouter, Depends, Query, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.api.response import pagination_meta, success_response
from app.api.v1.endpoints.auth_system import get_current_system_user
from app.models.activity_logs import ActivityLog
from app.models.users import SystemUser

router = APIRouter()


class ActivityLogCreateRequest(BaseModel):
    userName: str
    userRole: int
    module: str
    recorded: str
    userId: uuid.UUID | None = None


@router.get("/")
def list_activity_logs(
    page: int = Query(default=1, ge=1),
    pageSize: int = Query(default=50, ge=1, le=200),
    search: str | None = None,
    action: str | None = None,
    module: str | None = None,
    userId: uuid.UUID | None = None,
    db: Session = Depends(get_db),
    _: SystemUser = Depends(get_current_system_user),
):
    query = db.query(ActivityLog)
    if module:
        query = query.filter(ActivityLog.module == module)
    if userId:
        query = query.filter(ActivityLog.user_id == userId)
    if search:
        query = query.filter(ActivityLog.recorded.ilike(f"%{search}%"))
    if action:
        query = query.filter(ActivityLog.recorded.ilike(f"%{action}%"))

    total = query.count()
    items = query.order_by(ActivityLog.happended_at.desc()).offset((page - 1) * pageSize).limit(pageSize).all()

    data = [
        {
            "id": str(item.log_id),
            "userName": item.user_name,
            "userRole": item.user_role,
            "module": item.module,
            "recorded": item.recorded,
            "happendedAt": item.happended_at.isoformat(),
            "userId": str(item.user_id) if item.user_id else None,
        }
        for item in items
    ]
    return success_response("OK", data, pagination_meta(page, pageSize, total))


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_activity_log(
    payload: ActivityLogCreateRequest,
    db: Session = Depends(get_db),
    _: SystemUser = Depends(get_current_system_user),
):
    row = ActivityLog(
        user_name=payload.userName,
        user_role=payload.userRole,
        module=payload.module,
        recorded=payload.recorded,
        user_id=payload.userId,
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return success_response(
        "Created",
        {
            "id": str(row.log_id),
            "userName": row.user_name,
            "userRole": row.user_role,
            "module": row.module,
            "recorded": row.recorded,
            "happendedAt": row.happended_at.isoformat(),
            "userId": str(row.user_id) if row.user_id else None,
        },
    )
