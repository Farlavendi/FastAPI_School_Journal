from fastapi import APIRouter

from src.core.config import settings
from .v1 import router as router_api_v1

router = APIRouter(
    prefix=settings.api.prefix,
)
router.include_router(router_api_v1)
