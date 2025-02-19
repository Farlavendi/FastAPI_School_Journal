from typing import TYPE_CHECKING, Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .users import RoleEnum
from . import Base


if TYPE_CHECKING:
    from . import User, Class, Marks

import sqlalchemy as sa


class Student(Base):
    __tablename__ = "students"

    user_id: Mapped[int] = mapped_column(
        ForeignKey(
            column="users.id",
            ondelete="CASCADE",
            name="fk_student_user_id",
        ),
        nullable=False,
    )

    class_id: Mapped[int] = mapped_column(
        ForeignKey(
            column="classes.id",
            ondelete="CASCADE",
            name="fk_student_class_id",
        ),
        nullable=False,
    )

    user: Mapped["User"] = relationship(back_populates="student")
    # role: Mapped[RoleEnum] = mapped_column(
    #     sa.Enum(RoleEnum), default=RoleEnum.STUDENT, nullable=False
    # )
    class_: Mapped["Class"] = relationship(back_populates="students")
    marks: Mapped["Marks"] = relationship(back_populates="student")
