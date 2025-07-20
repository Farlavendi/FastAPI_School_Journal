from uuid import UUID

from pydantic import BaseModel, Field


class Marks(BaseModel):
    student_id: UUID
    maths: int | None = Field(None, ge=1, le=12)
    english: int | None = Field(None, ge=1, le=12)
    physics: int | None = Field(None, ge=1, le=12)
    chemistry: int | None = Field(None, ge=1, le=12)
    history: int | None = Field(None, ge=1, le=12)
    geography: int | None = Field(None, ge=1, le=12)
    literature: int | None = Field(None, ge=1, le=12)


class MarksUpdate(Marks):
    student_id: UUID = Field(...)
