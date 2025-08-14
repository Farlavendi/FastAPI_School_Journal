import secrets

from src.core.config import redis_client, settings
from src.core.models import User
from .send_email import send_email


async def send_verification_email(user: User):
    verification_token = secrets.token_urlsafe(32)
    verification_link = f"http://localhost:8000/docs#/verify_email?token={verification_token}"

    await send_email(
        recipient=user.email,
        subject="Verify your email for Fastapi Journal.",
        body="The link is valid for 10 minutes.\n"
             f"Follow the link: {verification_link}",
    )
    await redis_client.set(
        name=f"verification_token:{verification_token}",
        value=str(user.id),
        ex=settings.auth.verification_token_ttl
    )
