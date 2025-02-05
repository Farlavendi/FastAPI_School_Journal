from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING
from . import User

if TYPE_CHECKING:
    from . import Class


class Student(User):
    __tablename__ = "students"

    class_num: Mapped[int] = mapped_column(
        ForeignKey(
            "classes.class_num",
            ondelete="CASCADE",
            name="fk_student_class_num",
        ),
    )

    class_: Mapped["Class"] = relationship(back_populates="students")
