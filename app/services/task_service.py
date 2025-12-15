from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate


class TaskService:
    """Task business logic service - Example CRUD operations"""

    @staticmethod
    def get_by_id(db: Session, task_id: int, user_id: int) -> Task | None:
        """Get task by ID (only user's own tasks)"""
        return db.query(Task).filter(
            Task.id == task_id,
            Task.user_id == user_id
        ).first()

    @staticmethod
    def get_all(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> list[Task]:
        """Get all tasks for a user with pagination"""
        return db.query(Task).filter(
            Task.user_id == user_id
        ).offset(skip).limit(limit).all()

    @staticmethod
    def get_by_status(db: Session, user_id: int, status: str) -> list[Task]:
        """Get tasks by status"""
        return db.query(Task).filter(
            Task.user_id == user_id,
            Task.status == status
        ).all()

    @staticmethod
    def create(db: Session, task_in: TaskCreate, user_id: int) -> Task:
        """Create a new task"""
        try:
            db_task = Task(
                **task_in.model_dump(),
                user_id=user_id
            )
            db.add(db_task)
            db.commit()
            db.refresh(db_task)
            return db_task
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Error creating task",
            )

    @staticmethod
    def update(db: Session, task_id: int, task_in: TaskUpdate, user_id: int) -> Task:
        """Update task by ID"""
        db_task = TaskService.get_by_id(db, task_id, user_id)
        if not db_task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found",
            )

        update_data = task_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_task, field, value)

        try:
            db.add(db_task)
            db.commit()
            db.refresh(db_task)
            return db_task
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Error updating task",
            )

    @staticmethod
    def delete(db: Session, task_id: int, user_id: int) -> bool:
        """Delete task by ID"""
        db_task = TaskService.get_by_id(db, task_id, user_id)
        if not db_task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found",
            )

        try:
            db.delete(db_task)
            db.commit()
            return True
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Error deleting task",
            )

    @staticmethod
    def count_by_status(db: Session, user_id: int) -> dict:
        """Get count of tasks by status"""
        return {
            "pending": db.query(Task).filter(
                Task.user_id == user_id,
                Task.status == "pending"
            ).count(),
            "in_progress": db.query(Task).filter(
                Task.user_id == user_id,
                Task.status == "in_progress"
            ).count(),
            "completed": db.query(Task).filter(
                Task.user_id == user_id,
                Task.status == "completed"
            ).count(),
        }
