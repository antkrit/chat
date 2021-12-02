"""Chat service used to make database queries.

This module defines the following classes:
- `ChatService`, chat service
"""
from src.database.models import chat, message
from src.utils.exceptions import RecordNotFound


class ChatService:
    """Chat service used to make database queries."""

    @staticmethod
    async def get_chats(conn):
        """Get all chats.

        :param conn: `aiopg.sa.connection.SAConnection`
        :returns: list of chats
        """
        result = await conn.execute(chat.select())
        records = await result.fetchall()
        return records

    @staticmethod
    async def get_chat(conn, chat_uuid, n):
        """Get chat by uuid.

        :param conn: `aiopg.sa.connection.SAConnection`
        :param chat_uuid: chat uuid
        :param n: number of messages to load
        :returns: (chat, last n messages)
        """
        result = await conn.execute(
            chat.select()
                .where(chat.c.uuid == chat_uuid)
                .limit(1)
        )
        chat_record = await result.first()

        if not chat_record:
            raise RecordNotFound(
                'Chat with uuid: {} does not exists'.format(chat_uuid)
            )

        result = await conn.execute(
            message.select()
                   .where(message.c.chat_uuid == chat_uuid)
                   .order_by(message.c.id.desc())
                   .limit(n)
        )
        msg_records = await result.fetchall()
        return chat_record, reversed(msg_records)

    @staticmethod
    async def is_used(conn, title):
        """Check if chat title is not used.

        :param conn: `aiopg.sa.connection.SAConnection`
        :param title: chat title
        :returns: True if used, otherwise - False
        """
        result = await conn.execute(
            chat.select()
                .where(chat.c.title == title)
        )
        chat_name = await result.first()
        return chat_name is not None

    @staticmethod
    async def save_to_db(conn, title, description):
        """Save message to db.

        :param conn: `aiopg.sa.connection.SAConnection`
        :param title: chat title
        :param description: chat description
        """
        await conn.execute(
            chat.insert(values={
                'title': title,
                'description': description
            })
        )
