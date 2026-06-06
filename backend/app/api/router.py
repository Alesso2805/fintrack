from fastapi import APIRouter

from app.api.routes.auth import router as auth_router
from app.api.routes.financial_movements import router as financial_movements_router
from app.api.routes.health import router as health_router
from app.api.routes.imports import router as imports_router
from app.api.routes.investors import router as investors_router
from app.api.routes.movement_categories import router as movement_categories_router
from app.api.routes.users import router as users_router

api_router = APIRouter()
api_router.include_router(auth_router)
api_router.include_router(financial_movements_router)
api_router.include_router(health_router)
api_router.include_router(imports_router)
api_router.include_router(investors_router)
api_router.include_router(movement_categories_router)
api_router.include_router(users_router)
