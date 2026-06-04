from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.api.v1.endpoints.auth import get_current_user
from app.models.user import User
from app.schemas.task import TaskCreate, TaskRead, TaskUpdate
from app.services.task_service import TaskService

router = APIRouter()


@router.get("/", response_model=list[TaskRead])
def list_tasks(
    skip: int = 0,
    limit: int = 100,
    status_filter: str | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get all tasks for the current user
    
    - **skip**: Number of tasks to skip (pagination)
    - **limit**: Maximum number of tasks to return
    - **status_filter**: Filter by status (pending, in_progress, completed)

    Example:
        GET /api/v1/tasks/?status_filter=pending
        Header: Authorization: Bearer <your_token_here>
    """
    if status_filter:
        tasks = TaskService.get_by_status(db, current_user.id, status_filter)
    else:
        tasks = TaskService.get_all(db, current_user.id, skip=skip, limit=limit)
    return tasks


@router.post("/", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
def create_task(
    task_in: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Create a new task
    
    - **title**: Task title (required)
    - **description**: Task description (optional)
    - **status**: Task status - pending, in_progress, or completed (default: pending)

    Example:
        POST /api/v1/tasks/
        Header: Authorization: Bearer <your_token_here>
        {
            "title": "Finish Report",
            "description": "Complete the quarterly financial report",
            "status": "pending"
        }
    """
    task = TaskService.create(db, task_in, current_user.id)
    return task


@router.get("/stats")
def get_task_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get task statistics for current user
    
    Returns count of tasks by status

    Example:
        GET /api/v1/tasks/stats
        Header: Authorization: Bearer <your_token_here>
    """
    stats = TaskService.count_by_status(db, current_user.id)
    return {
        "user_id": current_user.id,
        "stats": stats,
        "total": sum(stats.values())
    }


@router.get("/{task_id}", response_model=TaskRead)
def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get task by ID
    
    - **task_id**: ID of the task to retrieve

    Example:
        GET /api/v1/tasks/1
        Header: Authorization: Bearer <your_token_here>
    """
    task = TaskService.get_by_id(db, task_id, current_user.id)
    if not task:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.put("/{task_id}", response_model=TaskRead)
def update_task(
    task_id: int,
    task_in: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Update task by ID
    
    - **task_id**: ID of the task to update
    - **task_in**: Task data to update (all fields optional)

    Example:
        PUT /api/v1/tasks/1
        Header: Authorization: Bearer <your_token_here>
        {
            "description": "Updated description"
        }
    """
    task = TaskService.update(db, task_id, task_in, current_user.id)
    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Delete task by ID
    
    - **task_id**: ID of the task to delete

    Example:
        DELETE /api/v1/tasks/1
        Header: Authorization: Bearer <your_token_here>
    """
    TaskService.delete(db, task_id, current_user.id)
    return None


# ============================================================================
# FORM-DATA ALTERNATIVE EXAMPLE
# ============================================================================
# If you want to accept form-data instead of JSON, use this pattern:
#
# from fastapi import Form
#
# @router.post("/form", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
# def create_task_form(
#     title: str = Form(...),              # Required form field
#     description: str = Form(None),       # Optional form field
#     status: str = Form("pending"),       # Form field with default value
#     db: Session = Depends(get_db),
#     current_user: User = Depends(get_current_user),
# ):
#     """
#     Create a new task using FORM DATA
#     
#     This accepts multipart/form-data instead of application/json
#     """
#     # Convert form fields to Pydantic schema
#     task_in = TaskCreate(
#         title=title,
#         description=description,
#         status=status
#     )
#     # Use the same service method
#     task = TaskService.create(db, task_in, current_user.id)
#     return task
#
# Usage in Postman/Thunder Client:
# - Set Body type to "form-data"
# - Add fields: title, description, status
# - Don't forget Authorization header with Bearer token
