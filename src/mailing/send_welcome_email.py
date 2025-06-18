from src.api.v1.users.crud import get_user_by_id
from src.core import db_helper
from src.core.models import User
from .send_email import send_email


async def send_welcome_email(user_id: int):
    async with db_helper.session_factory() as session:
        user: User = await get_user_by_id(
            session=session,
            user_id=user_id,
        )
        
    await send_email(
        recipient=user.email,
        subject="Fastapi-journal registration.",
        body=f"Dear {user.username},\n\nWelcome to Fastapi-journal!",
    )
