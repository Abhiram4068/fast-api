"""add foreign key relation ship in department with user model

Revision ID: c052c47d945c
Revises: 07f996ad01a8
Create Date: 2026-07-05 17:16:18.528387

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c052c47d945c'
down_revision: Union[str, Sequence[str], None] = '07f996ad01a8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # 1. Add column as nullable first
    op.add_column('departments', sa.Column('created_by', sa.UUID(), nullable=True))
    
    # 2. Get DB connection and try to find a default user to attribute existing departments to
    bind = op.get_bind()
    result = bind.execute(sa.text("SELECT id FROM users LIMIT 1")).fetchone()
    if result:
        default_user_id = result[0]
        bind.execute(
            sa.text("UPDATE departments SET created_by = :user_id WHERE created_by IS NULL"),
            {"user_id": default_user_id}
        )
    else:
        # If there are no users, we must clear the departments table to avoid NotNullViolation
        bind.execute(sa.text("DELETE FROM departments"))

    # 3. Alter column to be NOT NULL now that existing rows have a value
    op.alter_column('departments', 'created_by', nullable=False)

    # 4. Create foreign key relationship
    op.create_foreign_key(None, 'departments', 'users', ['created_by'], ['id'])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(None, 'departments', type_='foreignkey')
    op.drop_column('departments', 'created_by')
