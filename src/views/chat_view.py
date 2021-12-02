"""Chat views used to render chat template with users messages.

This module defines the following views:
- `chat`, function that defines chat view
"""
import uuid
import logging
import aiohttp_jinja2

from aiohttp import web, WSMsgType
from src.utils.flash import flash_get, flash_set
from src.utils.exceptions import RecordNotFound
from src.services import ChatService, MessageService


logger = logging.getLogger(__file__)


async def chat(request: web.Request):
    """Render `chat.html` template for url route `/chat/<uuid>` and endpoint `chat`.

    :param request: incoming request
    :raise `web.HTTPNotFound`: in case if uuid is wrong or chat with such \
    uuid does not exist
    :return: rendered template `chat.html` until the web socket is open, \
    `web.WebSocketResponse` after opening.
    """
    async with request.app['db'].acquire() as conn:
        try:
            chat_uuid = uuid.UUID(request.match_info['chat_uuid'])
            chat_uuid_hex = chat_uuid.hex
            chat_, messages = await ChatService.get_chat(
                conn, chat_uuid_hex, 100
            )

            if not request.app['websockets'].get(chat_uuid_hex, None):
                request.app['websockets'][chat_uuid_hex] = dict()

            name = request.rel_url.query.get('username')
            ws_by_name = request.app['websockets'][chat_uuid_hex].get(name, None)  # noqa: E501
            if not name:
                raise web.HTTPSeeOther(
                    str(request.app.router['index'].url_for())
                )
            if ws_by_name is not None:
                flash_set(
                    request,
                    'flash',
                    'Another person logged in under your nickname.'
                )
                await ws_by_name.close()

        except ValueError as err:
            # if unable convert chat_uuid to UUID
            raise web.HTTPNotFound(text=str(err))
        except RecordNotFound as err:
            # wrong chat_uuid
            raise web.HTTPNotFound(text=str(err))
        else:

            ws = web.WebSocketResponse()
            ws_ready = ws.can_prepare(request)

            if not ws_ready.ok:  # pragma: no cover
                flash = flash_get(request, 'flash')
                return aiohttp_jinja2.render_template('chat.html', request, {
                    'chat': chat_,
                    'messages': messages,
                    'flash': flash
                })

            await ws.prepare(request)

            logger.info('%s joined', name)

            for _ws in request.app['websockets'][chat_uuid_hex].values():
                await _ws.send_json({'body': '%s joined' % name})
            request.app['websockets'][chat_uuid_hex][name] = ws

            while True:
                msg = await ws.receive()

                if msg.type == WSMsgType.text and msg.data:
                    await MessageService.save_to_db(
                        conn, chat_uuid, msg.data, name
                    )
                    for _ws in request.app['websockets'][chat_uuid_hex].values():  # noqa: E501
                        await _ws.send_json({'body': msg.data, 'author': name})
                else:
                    break

            request.app['websockets'][chat_uuid_hex].pop(name, None)
            for _ws in request.app['websockets'][chat_uuid_hex].values():
                await _ws.send_json({'body': '%s disconnected' % name})
            logger.info('%s disconnected', name)

            return ws
