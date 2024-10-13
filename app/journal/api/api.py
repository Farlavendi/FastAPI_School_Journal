from fastapi import APIRouter

api_router = APIRouter(
    prefix="/api",
)


@api_router.get("/students")
def get_students():
    return ["Student_1", "Student_2", "Student_3"]
