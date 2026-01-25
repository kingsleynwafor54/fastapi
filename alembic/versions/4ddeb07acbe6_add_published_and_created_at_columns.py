"""add published and created_at columns

Revision ID: 4ddeb07acbe6
Revises: b2b5d86b67c2
Create Date: 2026-01-03 02:12:42.319026

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4ddeb07acbe6'
down_revision: Union[str, Sequence[str], None] = 'b2b5d86b67c2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "posts",
        sa.Column(
            "published",
            sa.Boolean,
            server_default=sa.text("TRUE"),
            nullable=False,
        ),
    )
    op.add_column(
        "posts",
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
    )
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("posts", "created_at")
    op.drop_column("posts", "published")
    pass
