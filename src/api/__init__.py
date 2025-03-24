from fastapi import APIRouter

from src.users.views import users_router
from .classes.views import classes_router

router = APIRouter()
router.include_router(router=classes_router, prefix="/classes")
router.include_router(router=users_router, prefix="/users")
