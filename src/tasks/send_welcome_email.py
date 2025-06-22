import logging

from src.core.taskiq import broker
from src.mailing.send_welcome_email import (
    send_welcome_email as send,
)

logger = logging.getLogger(__name__)


@broker.task
async def send_welcome_email(user_id: int) -> None:
    logger.info("Sending welcome email to user %s", user_id)
    await send(user_id=user_id)
