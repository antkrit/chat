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
        """Get all chats."""
        result = await conn.execute(chat.select())
        records = await result.fetchall()
        return records

    @staticmethod
    async def get_chat(conn, chat_uuid, n):
        """Get chat by uuid.

        :returns: (chat, last n messages)
        """
        result = await conn.execute(
            chat.select()
                .where(chat.c.uuid == chat_uuid)
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
