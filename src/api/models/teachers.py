from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING
from . import User

if TYPE_CHECKING:
    from . import Class


class Teacher(User):
    __tablename__ = "teachers"

    class_id: Mapped[int] = mapped_column(
        ForeignKey(
            "classes.id",
            ondelete="CASCADE",
            name="fk_teacher_class_id",
        ),
    )

    class_: Mapped["Class"] = relationship(back_populates="teachers")
