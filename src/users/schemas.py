from pydantic import BaseModel


class User(BaseModel):
    id: int
    email: str
    username: str
    first_name: str
    second_name: str
    last_name: str
