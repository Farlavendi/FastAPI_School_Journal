from typing import Optional

from pydantic import BaseModel, Field


class Marks(BaseModel):
    student_id: int
    maths: Optional[int] = Field(None, ge=1, le=12)
    english: Optional[int] = Field(None, ge=1, le=12)
    physics: Optional[int] = Field(None, ge=1, le=12)
    chemistry: Optional[int] = Field(None, ge=1, le=12)
    history: Optional[int] = Field(None, ge=1, le=12)
    geography: Optional[int] = Field(None, ge=1, le=12)
    literature: Optional[int] = Field(None, ge=1, le=12)


class MarksUpdate(Marks):
    pass
