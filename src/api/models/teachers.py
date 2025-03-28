from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import Base

if TYPE_CHECKING:
    from . import Class, User


class Teacher(Base):
    __tablename__ = "teachers"

    user_id: Mapped[int] = mapped_column(
        ForeignKey(
            column="users.id",
            ondelete="CASCADE",
            name="fk_teacher_user_id",
        ),
        nullable=False,
        index=True
    )

    class_id: Mapped[int] = mapped_column(
        ForeignKey(
            column="classes.id",
            ondelete="CASCADE",
            name="fk_teacher_class_id",
        ),
        nullable=False,
        unique=True,
        index=True
    )

    user: Mapped["User"] = relationship(back_populates="teacher")
    class_: Mapped["Class"] = relationship(back_populates="teacher", single_parent=True)
