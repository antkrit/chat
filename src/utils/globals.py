import os
import pathlib

BASEDIR = pathlib.Path(__file__).parents[2]
LOGS_FOLDER = os.path.join(BASEDIR, 'logs')
DEFAULT_LOGS_FORMAT = '%(asctime)s %(name)-14s %(levelname)s: ' \
                      '%(request_id_prefix)s%(message)s'
DB_DSN = "postgresql://{user}:{password}@{host}:{port}/{database}"
