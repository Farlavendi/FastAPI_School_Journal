from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.models import Base

if TYPE_CHECKING:
    from . import Student


class Marks(Base):
    __tablename__ = "marks"

    maths: Mapped[int] = mapped_column(nullable=True)
    english: Mapped[int] = mapped_column(nullable=True)
    physics: Mapped[int] = mapped_column(nullable=True)
    chemistry: Mapped[int] = mapped_column(nullable=True)
    history: Mapped[int] = mapped_column(nullable=True)
    geography: Mapped[int] = mapped_column(nullable=True)
    literature: Mapped[int] = mapped_column(nullable=True)

    student_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            column="students.id",
            ondelete="CASCADE",
            name="fk_marks_student_id",
        ),
        nullable=False,
        index=True,
    )

    student: Mapped["Student"] = relationship(back_populates="marks")
