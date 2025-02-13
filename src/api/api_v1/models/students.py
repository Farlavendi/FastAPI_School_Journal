from typing import TYPE_CHECKING, Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import User
from .users import RoleEnum

if TYPE_CHECKING:
    from . import Class
    from . import Marks
    from . import Profile

import sqlalchemy as sa


class Student(User):
    __tablename__ = "students"

    class_num: Mapped[int] = mapped_column(
        ForeignKey(
            "classes.class_num",
            ondelete="CASCADE",
            name="fk_student_class_num",
        ),
        nullable=False,
    )
    role: Mapped[RoleEnum] = mapped_column(sa.Enum(RoleEnum), default=RoleEnum.STUDENT, nullable=False)
    class_: Mapped["Class"] = relationship(back_populates="students")
    profile: Mapped[Optional["Profile"]] = relationship(back_populates="student")
    marks: Mapped["Marks"] = relationship(back_populates="student")
