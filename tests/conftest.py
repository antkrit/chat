import sys
import pytest
import asyncio

from src import init_app
from src.database import setup_db, teardown_db, create_tables, sample_data, drop_tables
from src.services import ChatService
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
        if sys.platform.startswith('win') and not isinstance(
                asyncio.get_event_loop_policy(),
                WindowsSelectorEventLoopPolicy
        ):
            asyncio.set_event_loop_policy(WindowsSelectorEventLoopPolicy())

    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


def pytest_addoption(parser):
    """Hook function to define new options."""
    parser.addoption("--config", action="store", default=TEST_CONFIG_PATH)


@pytest.fixture
async def client(loop, aiohttp_client, db, pytestconfig):
    """Return aiohttp client."""
    app = init_app(pytestconfig.getoption("config"))
    return await aiohttp_client(app), app


@pytest.fixture(scope='module')
def db(pytestconfig):
    """Raise db connection."""
    config = get_config(pytestconfig.getoption("config"))
    setup_db(config=config['postgres'])

    yield

    teardown_db(config=config['postgres'])


@pytest.fixture
def upgrade_and_populate_db():
    """Upgrade db to the latest revision and populate with some data."""
    create_tables()
    sample_data()

    yield

    drop_tables()
