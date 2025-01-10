from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING
from .base import Base

if TYPE_CHECKING:
    from .students import Student


class Class(Base):
    __tablename__ = "classes"

    class_num: Mapped[int] = mapped_column(unique=True)
    students: Mapped[list[Student]] = relationship(back_populates="class")
