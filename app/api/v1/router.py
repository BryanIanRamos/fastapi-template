from fastapi import APIRouter

from .endpoints import users, auth, tasks, ai_example

api_router = APIRouter()

# Authentication routes
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])

# User routes
api_router.include_router(users.router, prefix="/users", tags=["users"])

# Task routes (CRUD example)
api_router.include_router(tasks.router, prefix="/tasks", tags=["Tasks"])

# AI Tour Guide routes
api_router.include_router(ai_example.router, prefix="/ai", tags=["AI Tour Guide"])

__all__ = ["api_router"]
