import logging

import taskiq_fastapi
from taskiq import TaskiqEvents, TaskiqState
from taskiq_aio_pika import AioPikaBroker

from src.core.config import settings

logger = logging.getLogger(__name__)
broker = AioPikaBroker(
    url=settings.taskiq.url,
)
taskiq_fastapi.init(broker, "src.main:main_app")


@broker.on_event(TaskiqEvents.WORKER_STARTUP)
async def startup(state: TaskiqState) -> None:
    logging.basicConfig(
        level=settings.logging.log_level_value,
        format=settings.taskiq.log_format,
    )
