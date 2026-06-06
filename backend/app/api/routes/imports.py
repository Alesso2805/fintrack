import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.db.session import get_db_session
from app.models.imports import ImportBatch
from app.models.user import User
from app.repositories.audit_repository import ActionLogRepository
from app.repositories.financial_repository import FinancialMovementRepository
from app.repositories.import_repository import ImportBatchRepository
from app.schemas.imports import ImportBatchDetailsResponse, ImportBatchResponse
from app.services.import_service import ImportService

router = APIRouter(prefix="/imports", tags=["Imports"])


def get_import_service(session: AsyncSession = Depends(get_db_session)) -> ImportService:
    return ImportService(
        import_repo=ImportBatchRepository(session),
        movement_repo=FinancialMovementRepository(session),
        audit_repo=ActionLogRepository(session),
        session=session,
    )


@router.post("/csv", response_model=ImportBatchResponse, status_code=status.HTTP_201_CREATED)
async def upload_csv(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    import_service: ImportService = Depends(get_import_service),
):
    """
    Upload a CSV file of financial movements.
    The file should contain columns: investor_id, category_id, type, amount, currency, status, movement_date, description
    """
    if not file.filename or not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are allowed.")
    
    try:
        content = await file.read()
        content_str = content.decode("utf-8")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to read file: {e}")

    # For large files, background tasks should be used. For MVP, we run synchronously.
    import_batch = await import_service.process_csv(
        filename=file.filename,
        content=content_str,
        user_id=current_user.id
    )
    return import_batch


@router.get("", response_model=list[ImportBatchResponse])
async def list_imports(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    import_service: ImportService = Depends(get_import_service),
):
    """List all import batches."""
    return await import_service.get_import_batches(skip=skip, limit=limit)


@router.get("/{batch_id}", response_model=ImportBatchDetailsResponse)
async def get_import_batch(
    batch_id: str,
    current_user: User = Depends(get_current_user),
    import_service: ImportService = Depends(get_import_service),
):
    """Get details of a specific import batch."""
    try:
        uuid.UUID(batch_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid batch ID format")

    batch = await import_service.get_import_batch(batch_id)
    if not batch:
        raise HTTPException(status_code=404, detail="Import batch not found")
    return batch
