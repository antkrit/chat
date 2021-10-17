import sys
import pytest
import asyncio

from src import init_app
from src.database import setup_db, teardown_db, create_tables, sample_data, drop_tables
from src.utils.config import get_config
from src.utils.globals import TEST_CONFIG_PATH


@pytest.fixture(scope='session')
def loop():
    """Overwrite `pytest_asyncio` eventloop to fix Windows issue.

    Default implementation causes `NotImplementedError` on Windows with
    Python 3.8, because they changed default eventloop in 3.8.
    """
    try:
        from asyncio import WindowsSelectorEventLoopPolicy
    except ImportError:
        pass  # Can't assign a policy which doesn't exist.
    else:
        if not isinstance(
                asyncio.get_event_loop_policy(),
                WindowsSelectorEventLoopPolicy
        ) and sys.platform.startswith("win") and sys.version_info >= (3, 8):
            asyncio.set_event_loop_policy(WindowsSelectorEventLoopPolicy())

    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
async def client(loop, aiohttp_client, db):
    app = init_app(config_path=TEST_CONFIG_PATH)
    return await aiohttp_client(app)


@pytest.fixture(scope='module')
def db():
    config = get_config(TEST_CONFIG_PATH)
    setup_db(config['postgres'])

    yield

    teardown_db(config['postgres'])


@pytest.fixture
def upgrade_and_populate_db():
    create_tables()
    sample_data()

    yield

    drop_tables()
