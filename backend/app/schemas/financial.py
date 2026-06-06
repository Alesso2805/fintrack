from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

from app.models.financial import MovementStatus, MovementType


class InvestorBase(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    document_id: str | None = Field(default=None, max_length=100)
    email: EmailStr | None = None
    phone: str | None = Field(default=None, max_length=50)
    notes: str | None = None


class InvestorCreate(InvestorBase):
    pass


class InvestorUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    document_id: str | None = Field(default=None, max_length=100)
    email: EmailStr | None = None
    phone: str | None = Field(default=None, max_length=50)
    notes: str | None = None


class InvestorRead(InvestorBase):
    id: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class MovementCategoryBase(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    description: str | None = None


class MovementCategoryCreate(MovementCategoryBase):
    pass


class MovementCategoryUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = None


class MovementCategoryRead(MovementCategoryBase):
    id: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class FinancialMovementBase(BaseModel):
    investor_id: str
    category_id: str
    type: MovementType
    amount: Decimal = Field(gt=0, max_digits=14, decimal_places=2)
    currency: str = Field(min_length=3, max_length=3)
    status: MovementStatus
    movement_date: date
    description: str | None = None

    @field_validator("currency")
    @classmethod
    def normalize_currency(cls, value: str) -> str:
        return value.upper()


class FinancialMovementCreate(FinancialMovementBase):
    pass


class FinancialMovementUpdate(BaseModel):
    investor_id: str | None = None
    category_id: str | None = None
    type: MovementType | None = None
    amount: Decimal | None = Field(default=None, gt=0, max_digits=14, decimal_places=2)
    currency: str | None = Field(default=None, min_length=3, max_length=3)
    status: MovementStatus | None = None
    movement_date: date | None = None
    description: str | None = None

    @field_validator("currency")
    @classmethod
    def normalize_currency(cls, value: str | None) -> str | None:
        return value.upper() if value is not None else value


class FinancialMovementRead(FinancialMovementBase):
    id: str
    created_by: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
