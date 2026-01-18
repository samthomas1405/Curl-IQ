from fastapi import APIRouter
from app.api.v1 import auth, users, products, routines, routine_logs, outcomes, weather, dashboard

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(products.router, prefix="/products", tags=["products"])
api_router.include_router(routines.router, prefix="/routines", tags=["routines"])
api_router.include_router(routine_logs.router, prefix="/routine-logs", tags=["routine-logs"])
api_router.include_router(outcomes.router, prefix="/outcomes", tags=["outcomes"])
api_router.include_router(weather.router, prefix="/weather", tags=["weather"])
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])
