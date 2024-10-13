from pydantic import BaseModel


class Class(BaseModel):
    id: int
    number: int
