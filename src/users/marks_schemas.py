from pydantic import BaseModel


class Marks(BaseModel):
    student_id: int
    maths: int | None
    english: int | None
    physics: int | None
    history: int | None
    geography: int | None
    literature: int | None
