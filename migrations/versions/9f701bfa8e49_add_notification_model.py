"""Add Notification model

Revision ID: 9f701bfa8e49
Revises: b3ac2b2260e5
Create Date: 2025-05-09 16:05:39.710860

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9f701bfa8e49'
down_revision: Union[str, None] = 'b3ac2b2260e5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
