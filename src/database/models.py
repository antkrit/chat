"""Defines database tables.

Tables:
- `chat`, chat table with columns:
    [id, uuid, title, description, created_at]
- `message`, message table with columns:
    [id, uuid, body, author, created_at, chat_id]
"""
import uuid
from datetime import datetime
from sqlalchemy import (
    MetaData, Table, Column, Integer, String, DateTime, Text, ForeignKey
)
from sqlalchemy.dialects.postgresql import UUID

meta = MetaData()

chat = Table(
    'chat', meta,

    Column('id', Integer, primary_key=True),
    Column('uuid', UUID(as_uuid=True), index=True,
           nullable=False, unique=True, default=uuid.uuid4),
    Column('title', String(200), nullable=False, unique=True),
    Column('description', String(500)),
    Column('created_at', DateTime, nullable=False, default=datetime.utcnow)
)

message = Table(
    'message', meta,

    Column('id', Integer, primary_key=True),
    Column('uuid', UUID(as_uuid=True), index=True,
           nullable=False, unique=True, default=uuid.uuid4),
    Column('body', Text, nullable=False),
    Column('author', String(200), nullable=False, default="UNKNOWN"),
    Column('created_at', DateTime, nullable=False, default=datetime.utcnow),
    Column('chat_uuid', UUID(as_uuid=True), ForeignKey('chat.uuid'))
)
