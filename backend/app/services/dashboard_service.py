from datetime import date
from decimal import Decimal

from app.models.financial import MovementStatus, MovementType
from app.repositories.financial_repository import FinancialMovementRepository
from app.schemas.dashboard import BalanceByCurrency, CategoryDistribution, DashboardMetrics


class DashboardService:
    def __init__(self, movement_repo: FinancialMovementRepository) -> None:
        self.movement_repo = movement_repo

    async def get_dashboard_metrics(
        self,
        investor_id: str | None = None,
        category_id: str | None = None,
        status: MovementStatus | None = None,
        date_from: date | None = None,
        date_to: date | None = None,
    ) -> DashboardMetrics:
        # 1. Total movements
        movements = await self.movement_repo.list(
            investor_id=investor_id,
            category_id=category_id,
            status=status,
            date_from=date_from,
            date_to=date_to,
        )
        total_movements = len(movements)

        # 2. Balances by Currency
        balances_raw = await self.movement_repo.get_balances_by_currency(
            investor_id=investor_id,
            category_id=category_id,
            status=status,
            date_from=date_from,
            date_to=date_to,
        )
        
        balances = []
        for row in balances_raw:
            deposits = row.total_deposits or Decimal("0")
            withdrawals = row.total_withdrawals or Decimal("0")
            balance = deposits - withdrawals
            balances.append(
                BalanceByCurrency(
                    currency=row.currency,
                    total_deposits=deposits,
                    total_withdrawals=withdrawals,
                    balance=balance,
                )
            )

        # 3. Category Distribution
        categories_raw = await self.movement_repo.get_category_distribution(
            investor_id=investor_id,
            status=status,
            date_from=date_from,
            date_to=date_to,
        )
        
        category_distribution = []
        for row in categories_raw:
            category_distribution.append(
                CategoryDistribution(
                    category_id=str(row.category_id),
                    category_name=row.category_name,
                    total_amount=row.total_amount or Decimal("0"),
                )
            )

        return DashboardMetrics(
            balances=balances,
            category_distribution=category_distribution,
            total_movements=total_movements,
        )
