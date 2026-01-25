"""add content and publish to post table

Revision ID: 91c9b1b519b4
Revises: 13efadaa1e52
Create Date: 2026-01-03 01:36:03.471570

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '91c9b1b519b4'
down_revision:str='13efadaa1e52'
down_revision: Union[str, Sequence[str], None] = '13efadaa1e52'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts',sa.Column('content',sa.String(),nullable=False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts','content')
    pass
