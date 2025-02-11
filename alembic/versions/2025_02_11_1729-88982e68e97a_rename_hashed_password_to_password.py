"""Rename hashed_password to password.

Revision ID: 88982e68e97a
Revises: 17fbb1fc6b14
Create Date: 2025-02-11 17:29:55.845019

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "88982e68e97a"
down_revision: Union[str, None] = "17fbb1fc6b14"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("students", sa.Column("password", sa.String(), nullable=False))
    op.drop_constraint("uq_students_hashed_password", "students", type_="unique")
    op.create_unique_constraint(op.f("uq_students_password"), "students", ["password"])
    op.drop_column("students", "hashed_password")
    op.add_column("teachers", sa.Column("password", sa.String(), nullable=False))
    op.drop_constraint("uq_teachers_hashed_password", "teachers", type_="unique")
    op.create_unique_constraint(op.f("uq_teachers_password"), "teachers", ["password"])
    op.drop_column("teachers", "hashed_password")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "teachers", sa.Column("hashed_password", sa.VARCHAR(), autoincrement=False, nullable=False)
    )
    op.drop_constraint(op.f("uq_teachers_password"), "teachers", type_="unique")
    op.create_unique_constraint("uq_teachers_hashed_password", "teachers", ["hashed_password"])
    op.drop_column("teachers", "password")
    op.add_column(
        "students", sa.Column("hashed_password", sa.VARCHAR(), autoincrement=False, nullable=False)
    )
    op.drop_constraint(op.f("uq_students_password"), "students", type_="unique")
    op.create_unique_constraint("uq_students_hashed_password", "students", ["hashed_password"])
    op.drop_column("students", "password")
    # ### end Alembic commands ###
