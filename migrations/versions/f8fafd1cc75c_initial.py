"""initial

Revision ID: f8fafd1cc75c
Revises: a6f93953418a
Create Date: 2025-05-11 19:36:57.251332

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f8fafd1cc75c'
down_revision: Union[str, None] = 'a6f93953418a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
