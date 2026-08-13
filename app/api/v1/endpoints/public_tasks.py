from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.task import TaskCreate, TaskRead, TaskUpdate
from app.services.task_service import TaskService

router = APIRouter()

@router.get("/", response_model=list[TaskRead])
def list_public_tasks(
    skip: int = 0,
    limit: int = 100,
    status_filter: str | None = None,
    db: Session = Depends(get_db),
):
    """
    Get all tasks (Public - No Token Required)
    """
    # To avoid migration, we fetch tasks for the first available user
    from app.services.user_service import UserService
    users = UserService.get_all_users(db, limit=1)
    if not users:
        return []
    
    user_id = users[0].user_id
    if status_filter:
        tasks = TaskService.get_by_status(db, status=status_filter, user_id=user_id)
    else:
        tasks = TaskService.get_all(db, user_id=user_id, skip=skip, limit=limit)
    return tasks

@router.post("/", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
def create_public_task(
    task_in: TaskCreate,
    db: Session = Depends(get_db),
):
    """
    Create a new task (Public - No Token Required)
    """
    # To avoid migration, we use a fixed dummy user_id that must exist in the DB
    # In a real scenario, you'd create a 'System' user during setup
    from app.services.user_service import UserService
    system_user = UserService.get_all_users(db, limit=1)
    if not system_user:
        raise HTTPException(status_code=500, detail="No users found in database to assign public task to")
    
    user_id = system_user[0].user_id
    task = TaskService.create(db, task_in, user_id=user_id)
    return task

@router.get("/{task_id}", response_model=TaskRead)
def get_public_task(
    task_id: int,
    db: Session = Depends(get_db),
):
    """
    Get task by ID (Public - No Token Required)
    """
    # We remove the user_id filter to allow getting any task by ID
    task = TaskService.get_by_id(db, task_id, user_id=None)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.put("/{task_id}", response_model=TaskRead)
def update_public_task(
    task_id: int,
    task_in: TaskUpdate,
    db: Session = Depends(get_db),
):
    """
    Update task by ID (Public - No Token Required)
    """
    from app.models.task import Task
    db_task = TaskService.get_by_id(db, task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    update_data = task_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_task, field, value)
    
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_public_task(
    task_id: int,
    db: Session = Depends(get_db),
):
    """
    Delete task by ID (Public - No Token Required)
    """
    from app.models.task import Task
    db_task = TaskService.get_by_id(db, task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    db.delete(db_task)
    db.commit()
    return None
