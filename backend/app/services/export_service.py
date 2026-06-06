import csv
from datetime import date
from io import StringIO

from app.models.financial import MovementStatus, MovementType
from app.repositories.financial_repository import FinancialMovementRepository


class ExportService:
    def __init__(self, movement_repo: FinancialMovementRepository) -> None:
        self.movement_repo = movement_repo

    async def generate_movements_csv(
        self,
        investor_id: str | None = None,
        category_id: str | None = None,
        movement_type: MovementType | None = None,
        status: MovementStatus | None = None,
        date_from: date | None = None,
        date_to: date | None = None,
    ) -> str:
        movements = await self.movement_repo.list(
            investor_id=investor_id,
            category_id=category_id,
            movement_type=movement_type,
            status=status,
            date_from=date_from,
            date_to=date_to,
        )

        output = StringIO()
        fieldnames = [
            "id",
            "investor_id",
            "category_id",
            "type",
            "amount",
            "currency",
            "status",
            "movement_date",
            "description",
            "created_at",
        ]
        
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        writer.writeheader()

        for mov in movements:
            writer.writerow({
                "id": str(mov.id),
                "investor_id": str(mov.investor_id),
                "category_id": str(mov.category_id),
                "type": mov.type.value,
                "amount": str(mov.amount),
                "currency": mov.currency,
                "status": mov.status.value,
                "movement_date": mov.movement_date.isoformat(),
                "description": mov.description or "",
                "created_at": mov.created_at.isoformat() if mov.created_at else "",
            })

        return output.getvalue()
