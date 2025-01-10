from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Class(Base):
    __tablename__ = "classes"

    class_num: Mapped[int] = mapped_column(unique=True)
