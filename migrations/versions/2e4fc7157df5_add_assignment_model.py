"""Add Assignment model

Revision ID: 2e4fc7157df5
Revises: 9581fafd83a3
Create Date: 2025-05-08 21:21:38.812033

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2e4fc7157df5'
down_revision: Union[str, None] = '9581fafd83a3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
