"""add user table

Revision ID: 67aa00bf2fd4
Revises: 91c9b1b519b4
Create Date: 2026-01-03 01:45:10.147383

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '67aa00bf2fd4'
down_revision: Union[str, Sequence[str], None] = '91c9b1b519b4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
    "users",
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("email", sa.String, nullable=False),
    sa.Column("password", sa.String, nullable=False),
    sa.Column(
        "created_at",
        sa.TIMESTAMP(timezone=True),
        server_default=sa.text("now()"),
        nullable=False,
    ),
    sa.UniqueConstraint("email", name="uq_users_email"),
)

    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('users')
    pass
