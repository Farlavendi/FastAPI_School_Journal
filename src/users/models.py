from typing import Annotated

from fastapi import Path
from pydantic import BaseModel, EmailStr, Field


class User(BaseModel):
    email: Annotated[
        EmailStr,
        Path(unique=True),
        Field(..., alias='Email')
    ]

    username: Annotated[
        str,
        Path(min_length=1, max_length=150, unique=True),
        Field(..., alias='Username')
    ]

    first_name: Annotated[
        str,
        Path(min_length=1, max_length=150),
        Field(..., alias='First name')
    ]

    second_name: Annotated[
        str,
        Path(min_length=1, max_length=150),
        Field(alias='Second name')
    ]

    last_name: Annotated[
        str,
        Path(min_length=1, max_length=150),
        Field(..., alias='Last name')
    ]
