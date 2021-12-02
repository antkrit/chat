"""Create chat view used to render index template with list of chats.

This module defines the following views:
- `create_chat_post`, POST handler for create_chat
- `create_chat_get`, GET handler for create_chat
"""
import aiohttp_jinja2
from aiohttp import web
from src.services import ChatService
from src.utils.flash import flash_get, flash_set


@aiohttp_jinja2.template('create_chat.html')
async def create_chat_post(request: web.Request):
    """Render `create_chat.html` template for url route \
     POST `/create` and endpoint `create_chat_post`.

    :param request: `web.Request`
    :return: request context with list of chats
    """
    async with request.app['db'].acquire() as conn:
        data = await request.post()
        is_used = await ChatService.is_used(conn, title=data['name'])

        if not is_used:
            await ChatService.save_to_db(
                conn,
                data['name'],
                data['description']
            )

            flash_set(request, 'flash', 'Successfully created.')
            return web.HTTPSeeOther(
                str(request.app.router['index'].url_for())
            )

        flash_set(request, 'flash', 'A chat with this title already exists.')
        return web.HTTPSeeOther(
            str(request.app.router['create_chat'].url_for())
        )


@aiohttp_jinja2.template('create_chat.html')
async def create_chat_get(request: web.Request):
    """Render `create_chat.html` template for url route \
     GET `/create` and endpoint `create_chat`.

    :param request: `web.Request`
    :return: request context with list of chats
    """
    flash = flash_get(request, 'flash')
    if flash:
        return {'flash': flash}
