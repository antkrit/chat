import os
from src.utils.config import get_config
from src.utils.globals import (
    DEFAULT_CONFIG_PATH, TEST_CONFIG_PATH, DB_DSN,
    TEST_DB_URL, MAIN_DB_URL
)


def test_app_config(client):
    _, app = client

    config = app['config']
    assert config['postgres'] is not None
    assert config['app'] is not None


def test_development_config():
    assert os.path.exists(DEFAULT_CONFIG_PATH)
    config = get_config(DEFAULT_CONFIG_PATH)

    assert config['app']['debug']
    assert not config['app']['testing']
    assert DB_DSN.format(**config['postgres']) == MAIN_DB_URL


def test_testing_config():
    assert os.path.exists(TEST_CONFIG_PATH)
    config = get_config(TEST_CONFIG_PATH)

    assert config['app']['debug']
    assert config['app']['testing']
    assert DB_DSN.format(**config['postgres']) == TEST_DB_URL
