import logging

from pydantic.types import UUID

from src.api.v1.users.dependencies import user_by_id
from src.core.db_utils import TaskiqSessionDep
from src.core.taskiq import broker
from src.mailing.send_welcome_email import (
    send_welcome_email as send_welcome,
)

logger = logging.getLogger(__name__)


@broker.task
async def send_welcome_email(
    user_id: UUID,
    session: TaskiqSessionDep,
) -> None:
    user = await user_by_id(user_id=user_id, session=session)
    logger.info("Sending welcome email to user %s", user_id)
    await send_welcome(user=user)
