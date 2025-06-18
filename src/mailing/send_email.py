from email.message import EmailMessage

import aiosmtplib

from src.core.config import settings


async def send_email(
    recipient: str,
    subject: str,
    body: str,
):
    sender = settings.mailing.sender

    message = EmailMessage()
    message["From"] = sender
    message["To"] = recipient
    message["Subject"] = subject
    message.set_content(body)

    await aiosmtplib.send(
        message,
        sender=sender,
        recipients=[recipient],
        hostname=settings.mailing.host,
        port=settings.mailing.port,
    )
