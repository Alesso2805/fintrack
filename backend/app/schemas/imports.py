from datetime import date, datetime
from decimal import Decimal
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, constr

from app.models.financial import MovementStatus, MovementType
from app.models.imports import ImportBatchStatus


class ImportBatchBase(BaseModel):
    filename: str
    status: ImportBatchStatus
    total_rows: int
    successful_rows: int
    failed_rows: int


class ImportBatchResponse(ImportBatchBase):
    id: str
    created_by: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ImportBatchDetailsResponse(ImportBatchResponse):
    error_details: list[dict[str, Any]] | None = None


class CSVRow(BaseModel):
    investor_id: str
    category_id: str
    type: MovementType
    amount: Decimal = Field(gt=0, decimal_places=2)
    currency: constr(min_length=3, max_length=3)
    status: MovementStatus
    movement_date: date
    description: str | None = None
