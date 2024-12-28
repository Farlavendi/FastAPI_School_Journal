from typing import Annotated

from fastapi import Path
from pydantic import BaseModel, EmailStr, Field


class User(BaseModel):
   email: Annotated[
       EmailStr,
       Path(unique=True),
       Field(alias='email')
   ]

   username: Annotated[
       str,
       Path(le=150, unique=True),
       Field(alias='username')
   ]