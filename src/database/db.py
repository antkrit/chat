import aiopg.sa
from sqlalchemy import (
    MetaData, Table, Column, Integer, String, Date
)
from sqlalchemy.dialects.postgresql import UUID

__all__ = ['chat']  # list of all tables

meta = MetaData()


chat = Table(
    'chat', meta,

    Column('id', Integer, primary_key=True),
    Column('uuid', UUID, nullable=False, unique=True),
    Column('title', String(200), nullable=False, unique=True),
    Column('creation_date', Date, nullable=False)
)


async def get_question(conn, chat_id):
    result = await conn.execute(
        chat.select()
        .where(chat.c.id == chat_id))
    return await result.first()


def create_tables(engine):
    """Create database tables."""
    meta = MetaData()
    meta.create_all(bind=engine, tables=[chat])


async def pg_context(app):
    """Create postgresql context."""
    pg_conf = app['config']['postgres']
    engine = await aiopg.sa.create_engine(**pg_conf)
    app['db'] = engine

    yield

    app['db'].close()
    await app['db'].wait_closed()
