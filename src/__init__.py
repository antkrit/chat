"""
Sources root package.

Initializes web application and web service, contains following subpackages
and modules:

Subpackages:
- `database`: contains all database-related, including migrations
- `middlewares`: contains modules with request preprocessors/middlewares
- `rest`: contains modules with RESTful service implementation
- `schemas`: contains modules with serialization/deserialization schemas \
for models
- `static`: contains web application static files (scripts, styles, images)
- `templates`: contains web application html templates
- `utils`: contains modules with useful functions/classes to simplify code
- `views`: contains modules with web controllers/views
"""
import os
import sys
import logging
import asyncio
import jinja2
import aiohttp_jinja2

from aiohttp import web
from src.database.db import pg_context
from src.utils.globals import BASEDIR, LOGS_FOLDER, DEFAULT_LOGS_FORMAT
from src.utils.common import default_config, setup_middlewares, setup_routes
from src.utils.log import setup_log_record_factory, create_log_handler

# fix of an issue: https://github.com/aio-libs/aiopg/issues/678
try:
    from asyncio import WindowsSelectorEventLoopPolicy
except ImportError:
    pass  # Can't assign a policy which doesn't exist.
else:
    if not isinstance(
            asyncio.get_event_loop_policy(),
            WindowsSelectorEventLoopPolicy
    ):
        asyncio.set_event_loop_policy(WindowsSelectorEventLoopPolicy())

__author__ = 'Anton Krytskyi'
__maintainer__ = __author__

__email__ = 'mujanjagusav@gmail.com'
__license__ = 'MIT'
__version__ = '0.0.1'

__all__ = (
    '__author__',
    '__maintainer__',
    '__email__',
    '__license__',
    '__version__',
)

app = web.Application()
app['config'] = default_config

aiohttp_jinja2.setup(
    app,
    loader=jinja2.FileSystemLoader(os.path.join(BASEDIR, 'src', 'templates'))
)
setup_routes(app)
app.router.add_static(
    '/static/',
    path=os.path.join(BASEDIR, 'src', 'static'),
    name='static'
)
setup_middlewares(app)
app.cleanup_ctx.append(pg_context)

# logging
if not os.path.exists(LOGS_FOLDER):
    os.mkdir(LOGS_FOLDER)

logging.basicConfig(
    level=logging.DEBUG,
    format=DEFAULT_LOGS_FORMAT
)
setup_log_record_factory()

file_handler = create_log_handler(
    handler=logging.FileHandler,
    output=os.path.join(LOGS_FOLDER, 'app.log')
)
console_handler = create_log_handler(
    handler=logging.StreamHandler,
    output=sys.stdout
)

app.logger.handlers.clear()
app.logger.addHandler(file_handler)
app.logger.addHandler(console_handler)
app.logger.setLevel(logging.DEBUG)
