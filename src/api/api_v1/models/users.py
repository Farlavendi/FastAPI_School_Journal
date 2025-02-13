from enum import Enum
import sqlalchemy as sa
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from . import Base


class RoleEnum(Enum):
    STUDENT = "student"
    TEACHER = "teacher"
    SUPERUSER = "superuser"


class User(Base):
    __abstract__ = True

    email: Mapped[str] = mapped_column(
        unique=True,
    )
    username: Mapped[str] = mapped_column(
        unique=True,
    )
    password: Mapped[str] = mapped_column(
        unique=True,
    )
    first_name: Mapped[str] = mapped_column(String(50))
    second_name: Mapped[str | None] = mapped_column(
        String(50), default="", server_default=""
    )
    last_name: Mapped[str] = mapped_column(String(50))

    role: Mapped[RoleEnum] = mapped_column(sa.Enum(RoleEnum), default=RoleEnum.STUDENT, nullable=False)

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}, username={self.username!r})"

    def __repr__(self):
        return str(self)
