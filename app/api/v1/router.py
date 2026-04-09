from fastapi import APIRouter

from .endpoints import (
	activity_logs,
	auth_system,
	batches,
	biological_assets,
	dashboard,
	equipment_transactions,
	equipments,
	reports,
	users_system,
)

api_router = APIRouter()

# Authentication routes
api_router.include_router(auth_system.router, prefix="/auth", tags=["Authentication"])

# User routes
api_router.include_router(users_system.router, prefix="/users", tags=["Users"])

# Activity logs
api_router.include_router(activity_logs.router, prefix="/activity-logs", tags=["Activity Logs"])

# Batch management
api_router.include_router(batches.router, prefix="/batches", tags=["Batches"])

# Biological assets
api_router.include_router(biological_assets.router, prefix="/biological-assets", tags=["Biological Assets"])

# Equipment
api_router.include_router(equipments.router, prefix="/equipments", tags=["Equipment"])

# Equipment transactions
api_router.include_router(
	equipment_transactions.router,
	prefix="/equipment-transactions",
	tags=["Equipment Transactions"],
)

# Dashboard
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard"])

# Reports
api_router.include_router(reports.router, prefix="/reports", tags=["Reports"])

__all__ = ["api_router"]
