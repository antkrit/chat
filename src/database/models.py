import uuid
from datetime import datetime
from sqlalchemy import (
    MetaData, Table, Column, Integer, String, DateTime, Text, ForeignKey
)
from sqlalchemy.dialects.postgresql import UUID
from src.utils.exceptions import RecordNotFound

__all__ = ['chat', 'message']

meta = MetaData()

chat = Table(
    'chat', meta,

    Column('id', Integer, primary_key=True),
    Column('uuid', UUID(as_uuid=True),
           nullable=False, unique=True, default=uuid.uuid4),
    Column('title', String(200), nullable=False, unique=True),
    Column('description', String(500)),
    Column('created_at', DateTime, nullable=False, default=datetime.utcnow)
)

message = Table(
    'message', meta,

    Column('id', Integer, primary_key=True),
    Column('uuid', UUID(as_uuid=True),
           nullable=False, unique=True, default=uuid.uuid4),
    Column('body', Text, nullable=False),
    Column('created_at', DateTime, nullable=False, default=datetime.utcnow),
    Column('chat_id', Integer, ForeignKey('chat.id', ondelete='CASCADE'))
)


async def get_chat(conn, chat_uuid):
    result = await conn.execute(
        chat.select()
        .where(chat.c.uuid == chat_uuid)
    )
    chat_record = await result.first()

    if not chat_record:
        raise RecordNotFound(
            'Question with uuid: {} does not exists'.format(chat_uuid)
        )

    result = await conn.execute(
        message.select()
        .where(message.c.chat_id == chat_record.id)
        .order_by(message.c.id)
    )
    msg_records = await result.fetchall()

    return chat_record, msg_records
