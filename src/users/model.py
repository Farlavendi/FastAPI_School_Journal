from pydantic import EmailStr
from sqlalchemy import Integer, String

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class User(Base):
    __abstract__ = True
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        index=True,
    )
    email: Mapped[EmailStr] = mapped_column(
        EmailStr,
        unique=True,
        nullable=False,
        alias="email"
    )
    username: Mapped[str] = mapped_column(
        String,
        unique=True,
        nullable=False,
        min_length=3,
        max_length=25,
        alias="username"
    )
    first_name: Mapped[str] = mapped_column(
        String,
        nullable=False,
        min_length=3,
        max_length=25,
        alias="first_name",
    )
    second_name: Mapped[str] = mapped_column(
        String,
        nullable=True,
        min_length=3,
        max_length=25,
        alias="second_name",
    )
    last_name: Mapped[str] = mapped_column(
        String,
        nullable=False,
        min_length=3,
        max_length=25,
        alias="last_name",
    )
