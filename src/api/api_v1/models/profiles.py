from typing import TYPE_CHECKING, Optional

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, relationship, mapped_column

from . import Base

if TYPE_CHECKING:
    from . import Teacher, Student


class Profile(Base):
    __tablename__ = "profiles"

    id: Mapped[int] = mapped_column(primary_key=True)

    student_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("students.id", ondelete="CASCADE"), unique=True, nullable=True
    )
    teacher_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("teachers.id", ondelete="CASCADE"), unique=True, nullable=True
    )

    student: Mapped["Student"] = relationship(back_populates="profile")
    teacher: Mapped["Teacher"] = relationship(back_populates="profile")

    __table_args__ = (UniqueConstraint("student_id", "teacher_id"),)
