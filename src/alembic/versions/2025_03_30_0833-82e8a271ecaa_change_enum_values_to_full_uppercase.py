"""Recreate enums & change to full uppercase enum values.

Revision ID: 82e8a271ecaa
Revises: f15b957cc320
Create Date: 2025-03-30 08:33:26.331367

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '82e8a271ecaa'
down_revision: Union[str, None] = 'f15b957cc320'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("DROP TYPE IF EXISTS roleenum CASCADE")
    op.execute("DROP TYPE IF EXISTS subjectenum CASCADE")

    op.execute("""
        CREATE TYPE role_enum AS ENUM ('STUDENT', 'TEACHER', 'SUPERUSER')
    """)
    op.execute("""
        CREATE TYPE subject_enum AS ENUM ('MATH', 'ENGLISH', 'PHYSICS', 'CHEMISTRY', 'HISTORY', 'GEOGRAPHY', 'LITERATURE')
    """)

    op.add_column('users', sa.Column('role', sa.Enum(
        'STUDENT', 'TEACHER', 'SUPERUSER',
        name='role_enum'
    ), nullable=False))

    op.add_column('teachers', sa.Column('subject', sa.Enum(
        'MATH', 'ENGLISH', 'PHYSICS', 'CHEMISTRY', 'HISTORY', 'GEOGRAPHY', 'LITERATURE',
        name='subject_enum'
    ), nullable=True))

    op.create_index(op.f('ix_teachers_subject'), 'teachers', ['subject'], unique=False)
    op.create_index(op.f('ix_users_role'), 'users', ['role'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_teachers_subject'), table_name='teachers')
    op.drop_index(op.f('ix_users_role'), table_name='users')

    op.execute("DROP TYPE IF EXISTS role_enum CASCADE")
    op.execute("DROP TYPE IF EXISTS subject_enum CASCADE")

    op.execute("""
        CREATE TYPE roleenum AS ENUM ('STUDENT', 'TEACHER', 'SUPERUSER')
    """)
    op.execute("""
        CREATE TYPE subjectenum AS ENUM ('math', 'english', 'physics', 'chemistry', 'history', 'geography', 'literature')
    """)

    op.add_column('users', sa.Column('role', sa.Enum(
        'STUDENT', 'TEACHER', 'SUPERUSER',
        name='roleenum'
    ), nullable=False))

    op.add_column('teachers', sa.Column('subject', sa.Enum(
        'math', 'english', 'physics', 'chemistry', 'history', 'geography', 'literature',
        name='subjectenum'
    ), nullable=True))

    op.create_index(op.f('ix_users_role'), 'users', ['role'], unique=False)
    op.create_index(op.f('ix_teachers_subject'), 'teachers', ['subject'], unique=False)
    # ### end Alembic commands ###
