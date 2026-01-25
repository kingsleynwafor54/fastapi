"""add phone number column

Revision ID: 8b54ce1b63bb
Revises: df19bd2e22ec
Create Date: 2026-01-03 02:35:48.899148

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8b54ce1b63bb'
down_revision: Union[str, Sequence[str], None] = 'df19bd2e22ec'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
