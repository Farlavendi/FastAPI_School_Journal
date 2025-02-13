from typing import TYPE_CHECKING, Optional

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import User
from .users import RoleEnum

if TYPE_CHECKING:
    from . import Class
    from . import Profile

import sqlalchemy as sa


class Teacher(User):
    __tablename__ = "teachers"

    class_id: Mapped[int] = mapped_column(
        ForeignKey(
            "classes.id",
            ondelete="CASCADE",
            name="fk_teacher_class_id",
        ),
        nullable=False,
    )
    role: Mapped[RoleEnum] = mapped_column(sa.Enum(RoleEnum), default=RoleEnum.TEACHER, nullable=False)

    class_: Mapped["Class"] = relationship(back_populates="teacher", single_parent=True)
    profile: Mapped[Optional["Profile"]] = relationship(
        back_populates="teacher", uselist=False
    )

    __table_args__ = (UniqueConstraint("class_id"),)
