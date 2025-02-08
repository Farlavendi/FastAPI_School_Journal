from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, relationship, mapped_column

from . import Base

if TYPE_CHECKING:
    from . import Student


class Marks(Base):
    __tablename__ = "marks"

    maths: Mapped[int] = mapped_column()
    english: Mapped[int] = mapped_column()
    history: Mapped[int] = mapped_column()
    physics: Mapped[int] = mapped_column()
    geography: Mapped[int] = mapped_column()
    literature: Mapped[int] = mapped_column()

    student: Mapped["Student"] = relationship(back_populates="marks")
