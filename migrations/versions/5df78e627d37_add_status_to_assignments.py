"""add status to assignments

Revision ID: 5df78e627d37
Revises: f8fafd1cc75c
Create Date: 2025-05-11 19:38:09.492793

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5df78e627d37'
down_revision: Union[str, None] = 'f8fafd1cc75c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
