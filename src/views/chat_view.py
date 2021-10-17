import uuid
import aiohttp_jinja2
import src.database.models as db
from aiohttp import web
from src.utils.exceptions import RecordNotFound


@aiohttp_jinja2.template('chat.html')
async def chat(request):
    async with request.app['db'].acquire() as conn:
        try:
            chat_uuid = uuid.UUID(request.match_info['chat_uuid'])
            chats, messages = await db.get_chat(conn, chat_uuid)
        except ValueError as err:
            # if unable convert chat_uuid to UUID
            raise web.HTTPNotFound(text=str(err))
        except RecordNotFound as err:
            # wrong chat_uuid
            raise web.HTTPNotFound(text=str(err))
        return {
            'chats': chats,
            'messages': messages
        }
