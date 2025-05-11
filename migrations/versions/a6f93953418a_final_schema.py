"""Final schema

Revision ID: a6f93953418a
Revises: ea7bb2dc2d63
Create Date: 2025-05-09 23:48:00.924678

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a6f93953418a'
down_revision: Union[str, None] = 'ea7bb2dc2d63'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
