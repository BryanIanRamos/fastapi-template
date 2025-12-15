from fastapi import APIRouter

from .endpoints import users, auth, tasks

api_router = APIRouter()

# Authentication routes
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])

# User routes
api_router.include_router(users.router, prefix="/users", tags=["users"])

# Task routes (CRUD example)
api_router.include_router(tasks.router, prefix="/tasks", tags=["Tasks"])

__all__ = ["api_router"]
