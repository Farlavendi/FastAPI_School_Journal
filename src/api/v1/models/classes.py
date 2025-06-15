from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import Base

if TYPE_CHECKING:
    from . import Student, Teacher


class Class(Base):
    __tablename__ = "classes"

    class_num: Mapped[int] = mapped_column(unique=True, index=True)

    students: Mapped[list["Student"]] = relationship(back_populates="class_")
    teacher: Mapped["Teacher"] = relationship(back_populates="class_")
