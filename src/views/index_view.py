import aiohttp_jinja2
import src.database.models as db


@aiohttp_jinja2.template('index.html')
async def index(request):
    async with request.app['db'].acquire() as conn:
        cursor = await conn.execute(db.chat.select())
        records = await cursor.fetchall()
        chats = [dict(c) for c in records]
        return {'chats': chats}
