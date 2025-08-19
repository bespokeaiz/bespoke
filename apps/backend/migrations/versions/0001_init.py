"""init

Revision ID: 0001
Revises:
Create Date: 2025-08-19
"""
from alembic import op
import sqlalchemy as sa

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.create_table(
        "listings",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("title", sa.String(length=120), nullable=False),
        sa.Column("description", sa.Text, nullable=False),
        sa.Column("price_from", sa.Numeric(12, 2), nullable=False),
        sa.Column("city", sa.String(length=80), nullable=False),
        sa.Column("category", sa.String(length=80), nullable=False),
    )

def downgrade() -> None:
    op.drop_table("listings")
