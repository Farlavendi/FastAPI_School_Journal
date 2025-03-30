from pydantic import BaseModel


class Mark(BaseModel):
    maths: int | None
    english: int | None
    physics: int | None
    history: int | None
    geography: int | None
    literature: int | None
