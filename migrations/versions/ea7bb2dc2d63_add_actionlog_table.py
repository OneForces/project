"""Add ActionLog table

Revision ID: ea7bb2dc2d63
Revises: e1ed26ddf822
Create Date: 2025-05-09 23:03:11.533161

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ea7bb2dc2d63'
down_revision: Union[str, None] = 'e1ed26ddf822'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
