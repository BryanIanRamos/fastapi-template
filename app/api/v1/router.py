from fastapi import APIRouter

from .endpoints import users, auth, tasks, public_tasks

api_router = APIRouter()

# Authentication routes
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])

# User routes
api_router.include_router(users.router, prefix="/users", tags=["users"])

# Task routes (CRUD example)
api_router.include_router(tasks.router, prefix="/tasks", tags=["Tasks"])

# Public Task routes
api_router.include_router(public_tasks.router, prefix="/public-tasks", tags=["Public Tasks"])

__all__ = ["api_router"]
