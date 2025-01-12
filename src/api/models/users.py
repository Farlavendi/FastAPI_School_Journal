from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from . import Base


class User(Base):
    __abstract__ = True

    email: Mapped[str] = mapped_column(
        unique=True,
    )
    username: Mapped[str] = mapped_column(
        unique=True,
    )
    hashed_password: Mapped[str] = mapped_column(
        unique=True,
    )
    first_name: Mapped[str] = mapped_column(String(50))
    second_name: Mapped[str | None] = mapped_column(
        String(50), default="", server_default=""
    )
    last_name: Mapped[str] = mapped_column(String(50))
