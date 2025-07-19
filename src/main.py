import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse, RedirectResponse

from src.api import router as api_router
from src.auth.views import auth_router
from src.core.config import settings
from src.core.db_utils import db_helper
from src.core.gunicorn import Application, get_app_options
from src.core.taskiq import broker

logging.basicConfig(
    level=settings.logging.log_level_value,
    format=settings.logging.log_format,
)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    if not broker.is_worker_process:
        await broker.startup()

    yield

    await db_helper.dispose()

    if not broker.is_worker_process:
        await broker.shutdown()


main_app = FastAPI(
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
)
main_app.include_router(router=api_router)
main_app.include_router(router=auth_router)


@main_app.get("/")
async def root_and_redirect():
    redirect_url = RedirectResponse("/docs")
    return redirect_url


def main() -> None:
    app = Application(
        application=main_app,
        options=get_app_options(
            host=settings.gunicorn.host,
            port=settings.gunicorn.port,
            timeout=settings.gunicorn.timeout,
            workers=settings.gunicorn.workers,
            log_level=settings.logging.log_level,
        ),
    )
    app.run()


if __name__ == "__main__":
    main()
