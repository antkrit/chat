"""Message service used to make database queries.

This module defines the following classes:
- `MessageService`, message service
"""
from src.database.models import message


class MessageService:
    """Message service used to make database queries."""

    @staticmethod
    async def insert_message(conn, chat_uuid, body, author):
        """Save message to db."""
        await conn.execute(
            message.insert(values={
                'body': body,
                'author': author,
                'chat_uuid': chat_uuid
            })
        )
