import os
import pathlib
from sqlalchemy import create_engine
from src.utils.config import get_config

BASEDIR = pathlib.Path(__file__).parents[2]
LOGS_FOLDER = os.path.join(BASEDIR, 'logs')
STATIC_FOLDER = os.path.join(BASEDIR, 'src', 'static')
TEMPLATES_FOLDER = os.path.join(BASEDIR, 'src', 'templates')
DEFAULT_LOGS_FORMAT = '%(asctime)s %(name)-14s %(levelname)s: ' \
                      '%(request_id_prefix)s%(message)s'

DB_DSN = 'postgresql://{user}:{password}@{host}:{port}/{database}'
DEFAULT_CONFIG_PATH = os.path.join(BASEDIR, 'config', 'conf.yaml')
DEFAULT_CONFIG = get_config(DEFAULT_CONFIG_PATH)
MAIN_DB_URL = DB_DSN.format(**DEFAULT_CONFIG['postgres'])
main_engine = create_engine(MAIN_DB_URL)
# use only when an autocommit is required
main_engine_autocommit = create_engine(MAIN_DB_URL,
                                       isolation_level='AUTOCOMMIT')

TEST_CONFIG_PATH = os.path.join(BASEDIR, 'config', 'conf_test.yaml')
TEST_CONFIG = get_config(TEST_CONFIG_PATH)
TEST_DB_URL = DB_DSN.format(**TEST_CONFIG['postgres'])
engine_test_config = create_engine(TEST_DB_URL)
