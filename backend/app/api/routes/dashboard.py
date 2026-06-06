from datetime import date

from fastapi import APIRouter, Depends, Query

from app.api.deps import get_db_session
from app.api.deps import get_current_user
from app.models.financial import MovementStatus
from app.repositories.financial_repository import FinancialMovementRepository
from app.schemas.dashboard import DashboardMetrics
from app.services.dashboard_service import DashboardService

router = APIRouter()


def get_dashboard_service(session=Depends(get_db_session)) -> DashboardService:
    repo = FinancialMovementRepository(session)
    return DashboardService(repo)


@router.get("/metrics", response_model=DashboardMetrics)
async def get_metrics(
    investor_id: str | None = Query(None, description="Filter by investor ID"),
    category_id: str | None = Query(None, description="Filter by category ID"),
    status: MovementStatus | None = Query(None, description="Filter by status"),
    date_from: date | None = Query(None, description="Start date (YYYY-MM-DD)"),
    date_to: date | None = Query(None, description="End date (YYYY-MM-DD)"),
    current_user=Depends(get_current_user),
    dashboard_service: DashboardService = Depends(get_dashboard_service),
) -> DashboardMetrics:
    return await dashboard_service.get_dashboard_metrics(
        investor_id=investor_id,
        category_id=category_id,
        status=status,
        date_from=date_from,
        date_to=date_to,
    )
