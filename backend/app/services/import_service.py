import csv
from io import StringIO
from typing import Any

from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.audit import ActionLog
from app.models.financial import FinancialMovement
from app.models.imports import ImportBatch, ImportBatchStatus
from app.repositories.audit_repository import ActionLogRepository
from app.repositories.financial_repository import FinancialMovementRepository
from app.repositories.import_repository import ImportBatchRepository
from app.schemas.imports import CSVRow


class ImportService:
    def __init__(
        self,
        import_repo: ImportBatchRepository,
        movement_repo: FinancialMovementRepository,
        audit_repo: ActionLogRepository,
        session: AsyncSession,
    ):
        self.import_repo = import_repo
        self.movement_repo = movement_repo
        self.audit_repo = audit_repo
        self.session = session

    async def process_csv(self, filename: str, content: str, user_id: str) -> ImportBatch:
        # Create an initial PENDING batch
        import_batch = ImportBatch(
            filename=filename,
            status=ImportBatchStatus.PROCESSING,
            created_by=user_id,
            total_rows=0,
            successful_rows=0,
            failed_rows=0,
            error_details=[],
        )
        import_batch = await self.import_repo.create(import_batch)
        
        reader = csv.DictReader(StringIO(content))
        
        valid_movements: list[FinancialMovement] = []
        errors: list[dict[str, Any]] = []
        
        row_num = 1
        for row in reader:
            row_num += 1  # 1-indexed for the header, so data starts at 2
            try:
                # Validate the row against our Pydantic schema
                csv_row = CSVRow(**row)
                
                # Convert to SQLAlchemy model
                movement = FinancialMovement(
                    investor_id=csv_row.investor_id,
                    category_id=csv_row.category_id,
                    type=csv_row.type,
                    amount=csv_row.amount,
                    currency=csv_row.currency,
                    status=csv_row.status,
                    movement_date=csv_row.movement_date,
                    description=csv_row.description,
                    created_by=user_id,
                )
                valid_movements.append(movement)
            except ValidationError as e:
                import json
                # Store the pydantic errors in a readable format, e.json() ensures serializability
                errors.append({"row": row_num, "errors": json.loads(e.json())})
            except Exception as e:
                errors.append({"row": row_num, "errors": str(e)})

        total_rows = row_num - 1
        import_batch.total_rows = total_rows
        
        # Save valid movements to the database
        if valid_movements:
            for movement in valid_movements:
                await self.movement_repo.save(movement)
        
        import_batch.successful_rows = len(valid_movements)
        import_batch.failed_rows = len(errors)
        import_batch.error_details = errors
        
        if len(errors) == 0 and len(valid_movements) > 0:
            import_batch.status = ImportBatchStatus.COMPLETED
        elif len(valid_movements) > 0 and len(errors) > 0:
            import_batch.status = ImportBatchStatus.PARTIAL_SUCCESS
        else:
            import_batch.status = ImportBatchStatus.FAILED

        import_batch = await self.import_repo.update(import_batch)
        
        # Create an audit log
        action_log = ActionLog(
            user_id=user_id,
            action="IMPORT_CSV",
            entity_type="ImportBatch",
            entity_id=import_batch.id,
            details={
                "filename": filename,
                "status": import_batch.status,
                "total_rows": import_batch.total_rows,
                "successful_rows": import_batch.successful_rows,
                "failed_rows": import_batch.failed_rows,
            }
        )
        await self.audit_repo.create(action_log)
        
        return import_batch

    async def get_import_batches(self, skip: int = 0, limit: int = 100) -> list[ImportBatch]:
        return list(await self.import_repo.list_all(skip=skip, limit=limit))

    async def get_import_batch(self, batch_id: str) -> ImportBatch | None:
        return await self.import_repo.get_by_id(batch_id)
