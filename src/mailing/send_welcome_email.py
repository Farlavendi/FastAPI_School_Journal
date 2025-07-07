from src.core.models import User
from .send_email import send_email


async def send_welcome_email(user: User):
    await send_email(
        recipient=user.email,
        subject="Fastapi-journal registration.",
        body=f"Dear {user.username},\n\nWelcome to Fastapi-journal!",
    )
