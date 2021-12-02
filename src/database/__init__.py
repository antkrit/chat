"""Database package.

Defines functions to work with database, contains following subpackages
and modules:

Subpackages:
- `migrations`: contains database versions for migration

Modules:
- `models`: contains database tables
"""
import aiopg.sa
from faker import Faker
from sqlalchemy import MetaData, create_engine
from src.database.models import chat, message
from src.utils.globals import DB_DSN, TEST_CONFIG, main_engine_autocommit

# list of all tables
all_tables = (
    chat,
    message,
)


def setup_db(executor_engine=main_engine_autocommit,
             config=TEST_CONFIG['postgres']) -> None:
    """Connect to main db and then create new database, role."""
    db_name = config['database']
    db_user = config['user']
    db_password = config['password']

    with executor_engine.connect() as conn:
        conn.execute('DROP DATABASE IF EXISTS %s' % db_name)
        conn.execute('DROP ROLE IF EXISTS %s' % db_user)
        conn.execute('CREATE USER %s WITH PASSWORD \'%s\'' %  # noqa:Q003
                     (db_user, db_password))
        conn.execute('CREATE DATABASE %s ENCODING "UTF8"' % db_name)
        conn.execute('GRANT ALL PRIVILEGES ON DATABASE %s TO %s' %
                     (db_name, db_user))


def teardown_db(executor_engine=main_engine_autocommit,
                config=TEST_CONFIG['postgres']) -> None:
    """Connect to main db and drop database, role."""
    db_name = config['database']
    db_user = config['user']

    with executor_engine.connect() as conn:
        conn.execute("""
            SELECT pg_terminate_backend(pg_stat_activity.pid)
            FROM pg_stat_activity
            WHERE datname = '%s';""" % db_name)
        conn.execute('DROP DATABASE IF EXISTS %s' % db_name)
        conn.execute('DROP ROLE IF EXISTS %s' % db_user)


def create_tables(config=TEST_CONFIG['postgres'], tables=all_tables):
    """Create tables in a database.

    By default configured for engine with a test config.
    """
    engine = create_engine(
        DB_DSN.format(**config),
        isolation_level='AUTOCOMMIT'
    )

    meta = MetaData()
    meta.create_all(bind=engine, tables=tables)


def drop_tables(config=TEST_CONFIG['postgres'], tables=all_tables):
    """Delete tables from database.

    By default configured for engine with a test config.
    """
    engine = create_engine(
        DB_DSN.format(**config),
        isolation_level='AUTOCOMMIT'
    )

    meta = MetaData()
    meta.drop_all(bind=engine, tables=tables)


def sample_data(config=TEST_CONFIG['postgres']):
    """Populate database with some test data."""
    engine = create_engine(
        DB_DSN.format(**config),
        isolation_level='AUTOCOMMIT'
    )

    with engine.connect() as conn:
        conn.execute(chat.insert(values=[
            {
                'title': 'New chat',
                'description': Faker().text()
            },
            {
                'title': 'Another chat',
                'description': Faker().text()
            }
        ]))


async def pg_context(app):
    """Create postgresql context."""
    pg_conf = app['config']['postgres']
    engine = await aiopg.sa.create_engine(**pg_conf)
    app['db'] = engine

    yield

    app['db'].close()
    await app['db'].wait_closed()
