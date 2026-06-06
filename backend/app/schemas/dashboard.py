from decimal import Decimal
from typing import Any

from pydantic import BaseModel, Field


class BalanceByCurrency(BaseModel):
    currency: str = Field(..., description="The currency code, e.g., USD, EUR")
    total_deposits: Decimal = Field(..., description="Total deposited amount")
    total_withdrawals: Decimal = Field(..., description="Total withdrawn amount")
    balance: Decimal = Field(..., description="Current balance (deposits - withdrawals)")


class CategoryDistribution(BaseModel):
    category_id: str
    category_name: str
    total_amount: Decimal


class DashboardMetrics(BaseModel):
    balances: list[BalanceByCurrency] = Field(default_factory=list)
    category_distribution: list[CategoryDistribution] = Field(default_factory=list)
    total_movements: int = Field(..., description="Total number of movements matching the criteria")
