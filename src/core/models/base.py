from sqlalchemy import MetaData, types
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from uuid_utils import UUID, uuid4

from src.core.config import settings


class Base(DeclarativeBase):
    __abstract__ = True
    # id: Mapped[UUID] = mapped_column(
    #     UUID(as_uuid=True),
    #     primary_key=True,
    #     default=uuid7
    # )
    id: Mapped[UUID] = mapped_column(
        types.Uuid,
        primary_key=True,
        default=uuid4,
    )

    metadata = MetaData(naming_convention=settings.db.naming_convention)
