from enum import Enum
from typing import TYPE_CHECKING

import sqlalchemy as sa
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.models import Base

if TYPE_CHECKING:
    from src.api.v1.models import Student, Teacher


class RoleEnum(Enum):
    STUDENT = "STUDENT"
    TEACHER = "TEACHER"


class User(Base):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(
        unique=True,
        index=True,
    )
    username: Mapped[str] = mapped_column(
        unique=True,
        index=True,
    )
    password: Mapped[str] = mapped_column()
    first_name: Mapped[str] = mapped_column(String(100))
    second_name: Mapped[str | None] = mapped_column(
        String(50), default="", server_default="",
    )
    last_name: Mapped[str] = mapped_column(String(100))

    role: Mapped[RoleEnum] = mapped_column(
        sa.Enum(RoleEnum, name='role_enum'), nullable=False, index=True,
    )
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(default=False, nullable=False)
    is_verified: Mapped[bool] = mapped_column(default=False, nullable=False)

    student: Mapped["Student"] = relationship(back_populates="user", cascade="all, delete-orphan")
    teacher: Mapped["Teacher"] = relationship(back_populates="user", cascade="all, delete-orphan")

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}, username={self.username!r}, email={self.email!r})"

    def __repr__(self):
        return str(self)
