from fastapi import APIRouter

from .views import auth_router

router = APIRouter()
router.include_router(auth_router)
