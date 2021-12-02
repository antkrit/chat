"""Message service used to make database queries.

This module defines the following classes:
- `MessageService`, message service
"""
from src.database.models import message


class MessageService:
    """Message service used to make database queries."""

    @staticmethod
    async def save_to_db(conn, chat_uuid, body, author):
        """Save message to db.

        :param conn: `aiopg.sa.connection.SAConnection`
        :param chat_uuid: chat uuid
        :param body: message text
        :param author: author of the message
        """
        await conn.execute(
            message.insert(values={
                'body': body,
                'author': author,
                'chat_uuid': chat_uuid
            })
        )
