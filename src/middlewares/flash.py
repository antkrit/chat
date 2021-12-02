"""Defines preprocessor to set flash messages to session."""
from aiohttp import web
from aiohttp_session import get_session
from src.utils.globals import (
    FLASH_NEW_REQUEST_KEY, FLASH_OLD_REQUEST_KEY, FLASH_SESSION_KEY
)


@web.middleware
async def flash_middleware(request, handler):
    """Save new flash under FLASH_OLD_REQUEST_KEY after handled request."""
    session = await get_session(request)

    request[FLASH_OLD_REQUEST_KEY] = session.pop(FLASH_SESSION_KEY, {})
    request[FLASH_NEW_REQUEST_KEY] = {}

    try:
        return await handler(request)
    finally:
        session[FLASH_SESSION_KEY] = request[FLASH_NEW_REQUEST_KEY]
