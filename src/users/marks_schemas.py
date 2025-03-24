from pydantic import BaseModel


class Mark(BaseModel):
    maths: int | None
    english: int | None
    history: int | None
    physics: int | None
    geography: int | None
    literature: int | None
