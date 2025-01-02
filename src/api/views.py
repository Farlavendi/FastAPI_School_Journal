from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Path
from starlette import status

from api import crud
from api.models import Student

api_router = APIRouter(
    prefix="/api",
    tags=["Api"],
)


@api_router.get("/students/")
def get_students(student_id: Annotated[int, Path(ge=0)]):
    # if student_id not in students:
    #   raise HTTPException(status_code=404, detail="Not Found")
    # return {"student": students[student_id]}
    return "Some student"


# @api_router.post("/new_student/", status_code=status.HTTP_201_CREATED)
# def create_student(user: Student):
#     return crud.create_student(user)


@api_router.get("/students/{student_id}/")
def get_student_by_id(student_id: Annotated[int, Path(ge=0)]):
    return {
        "student": {
            "id": student_id,
        }
    }
