"""Add ActionLog model

Revision ID: 75c8671ec161
Revises: 9f701bfa8e49
Create Date: 2025-05-09 16:34:56.006418

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '75c8671ec161'
down_revision: Union[str, None] = '9f701bfa8e49'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
