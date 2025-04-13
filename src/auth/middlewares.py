from datetime import datetime, timezone

from fastapi import Request, HTTPException
from fastapi.logger import logger
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

from src.auth.token_mixin import create_access_token
from src.auth.utils import decode_jwt
from src.core import config
from src.core.db_utils import SessionDep
from src.users.crud import get_user_by_username

auth_jwt_config = config.AuthJWT()


class AutoRefreshTokenMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        access_token = request.cookies.get("access_token")
        refresh_token = request.cookies.get("refresh_token")

        if not access_token:
            return await call_next(request)

        try:
            payload = decode_jwt(access_token)
            exp = datetime.fromtimestamp(payload["exp"], tz=timezone.utc)
            now = datetime.now(tz=timezone.utc)
            remaining = (exp - now).total_seconds()

            if remaining < 60 and refresh_token:
                try:
                    refresh_payload = decode_jwt(refresh_token)
                    if refresh_payload.get("type") != "refresh":
                        logger.warning("Invalid refresh token type.")
                        return await call_next(request)

                    username = refresh_payload.get("sub")
                    if not username:
                        logger.warning("No username found in refresh token.")
                        return await call_next(request)

                    async with SessionDep as session:
                        user = await get_user_by_username(session=session, username=username)
                        if user:
                            new_access_token = create_access_token(user)
                            response = await call_next(request)
                            response.set_cookie(
                                key="access_token",
                                value=new_access_token,
                                httponly=True,
                                secure=True,
                                samesite="strict",
                                max_age=auth_jwt_config.access_token_expire_minutes * 60
                            )
                            return response
                        else:
                            logger.warning(f"User {username} not found.")
                            return await call_next(request)
                except Exception as e:
                    logger.error(f"Error refreshing token: {e}")
                    raise HTTPException(
                        status_code=401,
                        detail="Invalid or expired refresh token."
                    )

        except Exception as e:
            logger.error(f"Error handling access token: {e}")
            pass

        return await call_next(request)
