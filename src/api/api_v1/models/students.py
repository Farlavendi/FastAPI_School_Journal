from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import User

if TYPE_CHECKING:
    from . import Class
    from . import Marks
    from . import Profile


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
    class_: Mapped["Class"] = relationship(back_populates="students")
    profile: Mapped["Profile"] = relationship(back_populates="user")
    marks: Mapped["Marks"] = relationship(back_populates="student")
