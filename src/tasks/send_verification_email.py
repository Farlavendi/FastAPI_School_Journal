import logging
from uuid import UUID

from src.api.v1.users.dependencies import user_by_id
from src.core.db_utils import TaskiqSessionDep
from src.core.taskiq import broker
from src.mailing.send_verification_email import (
    send_verification_email as send_verification,
)

logger = logging.getLogger(__name__)


@broker.task
async def send_verification_email(
    user_id: UUID,
    session: TaskiqSessionDep,
) -> None:
    user = await user_by_id(user_id=user_id, session=session)
    logger.info("Sending verification email to user %s", user_id)
    await send_verification(user=user)
