from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column

from . import Base

if TYPE_CHECKING:
    from . import Student


class Marks(Base):
    __tablename__ = "marks"

    maths: Mapped[int] = mapped_column()
    english: Mapped[int] = mapped_column()
    physics: Mapped[int] = mapped_column()
    chemistry: Mapped[int] = mapped_column()
    history: Mapped[int] = mapped_column()
    geography: Mapped[int] = mapped_column()
    literature: Mapped[int] = mapped_column()

    student_id: Mapped[int] = mapped_column(
        ForeignKey(
            column="students.id",
            ondelete="CASCADE",
            name="fk_marks_student_id",
        ),
        nullable=False,
        index=True
    )

    student: Mapped["Student"] = relationship(back_populates="marks")
