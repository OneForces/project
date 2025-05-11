"""Add ActionLog model

Revision ID: e1ed26ddf822
Revises: 75c8671ec161
Create Date: 2025-05-09 16:42:06.609785

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e1ed26ddf822'
down_revision: Union[str, None] = '75c8671ec161'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
