from datetime import date

from fastapi import APIRouter, Depends, Query
from fastapi.responses import PlainTextResponse

from app.api.deps import get_db_session
from app.api.deps import get_current_user
from app.models.financial import MovementStatus, MovementType
from app.repositories.financial_repository import FinancialMovementRepository
from app.services.export_service import ExportService

router = APIRouter()


def get_export_service(session=Depends(get_db_session)) -> ExportService:
    repo = FinancialMovementRepository(session)
    return ExportService(repo)


@router.get("/movements/csv", response_class=PlainTextResponse)
async def export_movements_csv(
    investor_id: str | None = Query(None, description="Filter by investor ID"),
    category_id: str | None = Query(None, description="Filter by category ID"),
    movement_type: MovementType | None = Query(None, description="Filter by movement type"),
    status: MovementStatus | None = Query(None, description="Filter by status"),
    date_from: date | None = Query(None, description="Start date (YYYY-MM-DD)"),
    date_to: date | None = Query(None, description="End date (YYYY-MM-DD)"),
    current_user=Depends(get_current_user),
    export_service: ExportService = Depends(get_export_service),
):
    csv_content = await export_service.generate_movements_csv(
        investor_id=investor_id,
        category_id=category_id,
        movement_type=movement_type,
        status=status,
        date_from=date_from,
        date_to=date_to,
    )
    
    headers = {
        "Content-Disposition": "attachment; filename=movements_export.csv"
    }
    return PlainTextResponse(content=csv_content, media_type="text/csv", headers=headers)
