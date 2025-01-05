from fastapi import APIRouter
from .students.views import students_router

router = APIRouter()
router.include_router(router=students_router, prefix="/students")
