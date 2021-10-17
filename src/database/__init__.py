"""Database package.

Initializes web application and web service, contains following subpackages
and modules:

Subpackages:
- `migrations`: contains database versions for migration

Modules:
- `models`: contains database tables
"""
import aiopg.sa
from sqlalchemy import MetaData
from src.database.models import chat, message
from src.utils.globals import main_engine_autocommit, engine_test_config

# list of all tables
__all__ = (
    chat,
    message
)


def setup_db(config: dict) -> None:
    """Connect to main db and then create new database, role."""
    db_name = config['database']
    db_user = config['user']
    db_password = config['password']

    with main_engine_autocommit.connect() as conn:
        conn.execute('DROP DATABASE IF EXISTS %s' % db_name)
        conn.execute('DROP ROLE IF EXISTS %s' % db_user)
        conn.execute('CREATE USER %s WITH PASSWORD "%s"' %
                     (db_user, db_password))
        conn.execute('CREATE DATABASE %s ENCODING "UTF8"' % db_name)
        conn.execute('GRANT ALL PRIVILEGES ON DATABASE %s TO %s' %
                     (db_name, db_user))


def teardown_db(config: dict) -> None:
    """Connect to main db and drop database, role."""
    db_name = config['database']
    db_user = config['user']

    with main_engine_autocommit.connect() as conn:
        conn.execute("""
            SELECT pg_terminate_backend(pg_stat_activity.pid)
            FROM pg_stat_activity
            WHERE pg_stat_activity.datname = '%s'
            AND pid <> pg_backend_pid();""" % db_name)
        conn.execute('DROP DATABASE IF EXISTS %s' % db_name)
        conn.execute('DROP ROLE IF EXISTS %s' % db_user)


def create_tables(engine=engine_test_config, tables=__all__):
    """Create tables in a database.

    By default configured for engine with a test config.
    """
    meta = MetaData()
    meta.create_all(bind=engine, tables=tables)


def drop_tables(engine=engine_test_config, tables=__all__):
    """Delete tables from database.

    By default configured for engine with a test config.
    """
    meta = MetaData()
    meta.create_all(bind=engine, tables=tables)


def sample_data(engine=engine_test_config):
    """Populate database with some test data."""
    with engine.connect() as conn:
        conn.execute(chat.insert(), [
            {
                'title': 'New chat',
                'description': 'Here is something interesting.'
            }
        ])
        conn.execute(message.insert(), [
            {'body': 'Hi', 'chat_id': 1},
            {'body': 'Hello', 'chat_id': 1},
        ])


async def pg_context(app):
    """Create postgresql context."""
    pg_conf = app['config']['postgres']
    engine = await aiopg.sa.create_engine(**pg_conf)
    app['db'] = engine

    yield

    app['db'].close()
    await app['db'].wait_closed()
