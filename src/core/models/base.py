from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from src.core.config import settings


class Base(DeclarativeBase):
    __abstract__ = True
    # id: Mapped[UUID] = mapped_column(
    #     UUID(as_uuid=True),
    #     primary_key=True,
    #     default=uuid7
    # )
    id: Mapped[int] = mapped_column(
        primary_key=True,
    )

    metadata = MetaData(naming_convention=settings.db.naming_convention)
