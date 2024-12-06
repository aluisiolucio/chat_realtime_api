"""Add creator_id in rooms table

Revision ID: 24d95f1c2847
Revises: b4652890743b
Create Date: 2024-12-05 17:02:43.252156

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import sqlite


# revision identifiers, used by Alembic.
revision: str = '24d95f1c2847'
down_revision: Union[str, None] = 'b4652890743b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Detecting if the database is SQLite
    bind = op.get_bind()
    if isinstance(bind.dialect, sqlite.dialect):
        # SQLite-specific behavior
        with op.batch_alter_table('rooms') as batch_op:
            batch_op.add_column(sa.Column('creator_id', sa.Uuid(), nullable=False))
            batch_op.create_foreign_key(
                'fk_rooms_creator_id',  # Explicit name for the constraint
                'users',  # Referenced table
                ['creator_id'],  # Local column
                ['id']  # Referenced column
            )

        with op.batch_alter_table('users') as batch_op:
            batch_op.drop_column('updated_at')
    else:
        # For other databases
        op.add_column('rooms', sa.Column('creator_id', sa.Uuid(), nullable=False))
        op.create_foreign_key(
            'fk_rooms_creator_id',  # Explicit name for the constraint
            'rooms',  # Table
            'users',  # Referenced table
            ['creator_id'],  # Local column
            ['id']  # Referenced column
        )
        op.drop_column('users', 'updated_at')


def downgrade() -> None:
    bind = op.get_bind()
    if isinstance(bind.dialect, sqlite.dialect):
        # SQLite-specific behavior
        with op.batch_alter_table('users') as batch_op:
            batch_op.add_column(sa.Column('updated_at', sa.DATETIME(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False))

        with op.batch_alter_table('rooms') as batch_op:
            batch_op.drop_constraint('fk_rooms_creator_id', type_='foreignkey')
            batch_op.drop_column('creator_id')
    else:
        # For other databases
        op.add_column('users', sa.Column('updated_at', sa.DATETIME(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False))
        op.drop_constraint('fk_rooms_creator_id', 'rooms', type_='foreignkey')
        op.drop_column('rooms', 'creator_id')
