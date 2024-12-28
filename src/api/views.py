from typing import Annotated

from fastapi import APIRouter, Path

from api.models import Student

api_router = APIRouter(
    prefix="/api",
    tags=["Api"],
)


@api_router.get("/students/")
def get_students():
    return ["Student_1", "Student_2", "Student_3"]


@api_router.post("/new_student/")
def create_student(student: Student):
    return student


@api_router.get("/students/{student_id}/")
def get_student_by_id(student_id: Annotated[int, Path(ge=0)]):
    return {
        "student": {
            "id": student_id,
        }
    }
