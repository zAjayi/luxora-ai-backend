"""Require passwords for users.

Revision ID: c7a8b9d0e1f2
Revises: f6e7d8c9b0a1
Create Date: 2026-09-18 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op


revision: str = "c7a8b9d0e1f2"
down_revision: Union[str, Sequence[str], None] = "f6e7d8c9b0a1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column("users", "hashed_password", nullable=False)


def downgrade() -> None:
    op.alter_column("users", "hashed_password", nullable=True)