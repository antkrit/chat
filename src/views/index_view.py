"""Index view used to render index template with list of chats.

This module defines the following views:
- `index`, function that defines index view
"""
import aiohttp_jinja2
from aiohttp import web
from src.services import ChatService


@aiohttp_jinja2.template('index.html')
async def index(request: web.Request):
    """Render `index.html` template for url route `/` and endpoint `index`.

    :param request: incoming request
    :return: request context with list of chats
    """
    async with request.app['db'].acquire() as conn:
        chats = await ChatService.get_chats(conn)
        return {'chats': chats}
