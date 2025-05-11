"""Add response_file to Assignment

Revision ID: b3ac2b2260e5
Revises: 2e4fc7157df5
Create Date: 2025-05-09 01:12:00.804193

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b3ac2b2260e5'
down_revision: Union[str, None] = '2e4fc7157df5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
