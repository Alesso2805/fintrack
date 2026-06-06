"""create financial entities

Revision ID: 20260606_0002
Revises: 20260605_0001
Create Date: 2026-06-06
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20260606_0002"
down_revision: str | None = "20260605_0001"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "investors",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("document_id", sa.String(length=100), nullable=True),
        sa.Column("email", sa.String(length=255), nullable=True),
        sa.Column("phone", sa.String(length=50), nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("document_id"),
    )
    op.create_index(op.f("ix_investors_name"), "investors", ["name"], unique=True)

    op.create_table(
        "movement_categories",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_movement_categories_name"),
        "movement_categories",
        ["name"],
        unique=True,
    )

    op.create_table(
        "financial_movements",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("investor_id", sa.String(length=36), nullable=False),
        sa.Column("category_id", sa.String(length=36), nullable=False),
        sa.Column(
            "type",
            sa.Enum("deposit", "withdrawal", "dividend", "fee", "adjustment", name="movement_type", native_enum=False),
            nullable=False,
        ),
        sa.Column("amount", sa.Numeric(14, 2), nullable=False),
        sa.Column("currency", sa.String(length=3), nullable=False),
        sa.Column(
            "status",
            sa.Enum("pending", "completed", "cancelled", name="movement_status", native_enum=False),
            nullable=False,
        ),
        sa.Column("movement_date", sa.Date(), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("created_by", sa.String(length=36), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["category_id"], ["movement_categories.id"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(["created_by"], ["users.id"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(["investor_id"], ["investors.id"], ondelete="RESTRICT"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_financial_movements_category_id"), "financial_movements", ["category_id"])
    op.create_index(op.f("ix_financial_movements_investor_id"), "financial_movements", ["investor_id"])
    op.create_index(op.f("ix_financial_movements_movement_date"), "financial_movements", ["movement_date"])
    op.create_index(op.f("ix_financial_movements_status"), "financial_movements", ["status"])
    op.create_index(op.f("ix_financial_movements_type"), "financial_movements", ["type"])


def downgrade() -> None:
    op.drop_index(op.f("ix_financial_movements_type"), table_name="financial_movements")
    op.drop_index(op.f("ix_financial_movements_status"), table_name="financial_movements")
    op.drop_index(op.f("ix_financial_movements_movement_date"), table_name="financial_movements")
    op.drop_index(op.f("ix_financial_movements_investor_id"), table_name="financial_movements")
    op.drop_index(op.f("ix_financial_movements_category_id"), table_name="financial_movements")
    op.drop_table("financial_movements")
    op.drop_index(op.f("ix_movement_categories_name"), table_name="movement_categories")
    op.drop_table("movement_categories")
    op.drop_index(op.f("ix_investors_name"), table_name="investors")
    op.drop_table("investors")
