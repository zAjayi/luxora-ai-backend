"""Add repurpose job title

Revision ID: b4b3f5c2f1e4
Revises: dd9593d98ecd
Create Date: 2026-08-01 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b4b3f5c2f1e4'
down_revision: Union[str, Sequence[str], None] = 'dd9593d98ecd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('repurpose_jobs', sa.Column('title', sa.String(length=255), nullable=True))


def downgrade() -> None:
    op.drop_column('repurpose_jobs', 'title')