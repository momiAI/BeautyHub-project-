"""add model MasterRequest

Revision ID: 7409151610c6
Revises: abe22abb7f39
Create Date: 2025-12-12 10:19:54.813385

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "7409151610c6"
down_revision: Union[str, Sequence[str], None] = "abe22abb7f39"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "masterrequest", sa.Column("bio_short", sa.String(length=50), nullable=False)
    )
    op.add_column(
        "masterrequest",
        sa.Column("specializations", sa.ARRAY(sa.String()), nullable=False),
    )
    op.add_column(
        "masterrequest", sa.Column("portfolio", sa.ARRAY(sa.String()), nullable=True)
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_column("masterrequest", "portfolio")
    op.drop_column("masterrequest", "specializations")
    op.drop_column("masterrequest", "bio_short")
