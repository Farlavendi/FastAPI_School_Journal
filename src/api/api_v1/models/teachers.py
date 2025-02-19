from typing import TYPE_CHECKING, Optional

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .users import RoleEnum
from . import Base


if TYPE_CHECKING:
    from . import Class, User

import sqlalchemy as sa


class Teacher(Base):
    __tablename__ = "teachers"

    # user_id: Mapped[int] = mapped_column(
    #         ForeignKey(
    #             column="users.id",
    #             ondelete="CASCADE",
    #             name="fk_student_user_id",
    #         ),
    #         nullable=False,
    #     )


    class_id: Mapped[int] = mapped_column(
        ForeignKey(
            "classes.id",
            ondelete="CASCADE",
            name="fk_teacher_class_id",
        ),
        nullable=False,
    )

    # user: Mapped["User"] = relationship(back_populates="student")

    role: Mapped[RoleEnum] = mapped_column(sa.Enum(RoleEnum), default=RoleEnum.TEACHER, nullable=False)

    class_: Mapped["Class"] = relationship(back_populates="teacher", single_parent=True)

    __table_args__ = (UniqueConstraint("class_id"),)
