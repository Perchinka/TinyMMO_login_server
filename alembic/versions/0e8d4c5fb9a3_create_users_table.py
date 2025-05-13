"""create users table

Revision ID: 0e8d4c5fb9a3
Revises:
Create Date: 2025-05-13 16:38:08.801300

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "0e8d4c5fb9a3"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
          username VARCHAR PRIMARY KEY,
          password_hash VARCHAR NOT NULL
        );
        """
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("users")
