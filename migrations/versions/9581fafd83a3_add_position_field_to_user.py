"""Add position field to User

Revision ID: 9581fafd83a3
Revises: c4e03b7a5f2c
Create Date: 2025-05-08 20:53:58.968744

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9581fafd83a3'
down_revision: Union[str, None] = 'c4e03b7a5f2c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
