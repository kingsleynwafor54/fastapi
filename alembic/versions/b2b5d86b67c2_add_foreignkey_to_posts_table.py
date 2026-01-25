"""add foreignkey to posts table

Revision ID: b2b5d86b67c2
Revises: 67aa00bf2fd4
Create Date: 2026-01-03 01:53:29.097735

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b2b5d86b67c2'
down_revision: Union[str, Sequence[str], None] = '67aa00bf2fd4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts',sa.Column('owner_id',sa.Integer(),nullable=False))
    op.create_foreign_key("post_users_fk",source_table="posts"
                          ,referent_table="users",local_cols=['owner_id'],
                          remote_cols=['id'],ondelete='CASCADE')
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('post_users_fk',table_name='posts')
    op.drop_column('posts','owner_id')
    pass
