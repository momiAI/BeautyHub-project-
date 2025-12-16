"""fix models

Revision ID: abe22abb7f39
Revises: c1c02999ff29
Create Date: 2025-12-12 09:48:54.042710

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "abe22abb7f39"
down_revision: Union[str, Sequence[str], None] = "c1c02999ff29"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.create_table(
        "masterrequest",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("id_user", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["id_user"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.alter_column(
        "timetable",
        "day_of_week",
        existing_type=sa.VARCHAR(length=10),
        type_=sa.Enum(
            "monday",
            "tuesday",
            "wednesday",
            "thursday",
            "friday",
            "saturday",
            "sunday",
            name="weekday",
            native_enum=False,
        ),
        existing_nullable=False,
    )
    op.create_unique_constraint(
        "uq_master_day", "timetable", ["id_master", "day_of_week"]
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint("uq_master_day", "timetable", type_="unique")
    op.alter_column(
        "timetable",
        "day_of_week",
        existing_type=sa.Enum(
            "monday",
            "tuesday",
            "wednesday",
            "thursday",
            "friday",
            "saturday",
            "sunday",
            name="weekday",
            native_enum=False,
        ),
        type_=sa.VARCHAR(length=10),
        existing_nullable=False,
    )
    op.drop_table("masterrequest")
