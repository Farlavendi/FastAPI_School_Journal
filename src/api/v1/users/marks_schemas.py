from pydantic import BaseModel, Field
from pydantic.types import UUID


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
    pass
