"""Sources root package.

Initializes web application and web service, contains following subpackages
and modules:

Subpackages:
- `database`: contains everything related to database, including migrations
- `middlewares`: contains modules with request preprocessors/middlewares
- `rest`: contains modules with RESTful service implementation
- `schemas`: contains modules with serialization/deserialization schemas \
for models
- `static`: contains web application static files (scripts, styles, images)
- `templates`: contains web application html templates
- `utils`: contains modules with useful functions/classes to simplify code
- `views`: contains modules with web controllers
"""
import os
import sys
import logging
import asyncio
import jinja2
import aiohttp_jinja2

from aiohttp import web
from src.database import pg_context
from src.views import index_view, chat_view
from src.middlewares import log as ml, errors as me
from src.utils.globals import (
    BASEDIR, LOGS_FOLDER, DEFAULT_LOGS_FORMAT, DEFAULT_CONFIG_PATH
)
from src.utils.config import get_config
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
    ) and sys.platform.startswith('win') and sys.version_info >= (3, 8):
        asyncio.set_event_loop_policy(WindowsSelectorEventLoopPolicy())

__author__ = 'Anton Krytskyi'
__maintainer__ = __author__

__email__ = 'mujanjagusav@gmail.com'
__license__ = 'MIT'
__version__ = '0.1.0'

__all__ = (
    '__author__',
    '__maintainer__',
    '__email__',
    '__license__',
    '__version__',
)


def setup_middlewares(curr_app):
    """Add custom middlewares to app middlewares."""
    curr_app.middlewares.append(ml.add_request_id_middleware)
    curr_app.middlewares.append(me.error_middleware)


def setup_routes(curr_app):
    """Add routes to app router."""
    curr_app.router.add_get('/', index_view.index, name='index')
    curr_app.router.add_get('/chat/{chat_uuid}', chat_view.chat, name='chat')
    curr_app.router.add_static(
        '/static/',
        path=os.path.join(BASEDIR, 'src', 'static'),
        name='static'
    )


def setup_logging():
    """Add file handler and stream handler to default app logger."""
    if not os.path.exists(LOGS_FOLDER):
        os.mkdir(LOGS_FOLDER)

    logging.basicConfig(
        level=logging.DEBUG,
        format=DEFAULT_LOGS_FORMAT
    )
    setup_log_record_factory()

    console_handler = create_log_handler(
        handler=logging.StreamHandler,
        output=sys.stdout
    )

    # aiohttp
    main_logger = logging.getLogger('aiohttp')
    main_logger.handlers.clear()
    main_logger.addHandler(create_log_handler(
        handler=logging.FileHandler,
        output=os.path.join(LOGS_FOLDER, 'app.log')
    ))
    main_logger.addHandler(console_handler)
    main_logger.setLevel(logging.DEBUG)
    main_logger.propagate = False

    # aiohttp.access
    access_logger = logging.getLogger('aiohttp.access')
    access_logger.handlers.clear()
    access_logger.addHandler(create_log_handler(
        handler=logging.FileHandler,
        output=os.path.join(LOGS_FOLDER, 'access.log')
    ))
    access_logger.setLevel(logging.DEBUG)

    # aiohttp.server
    server_logger = logging.getLogger('aiohttp.server')
    server_logger.handlers.clear()
    server_logger.addHandler(create_log_handler(
        handler=logging.FileHandler,
        output=os.path.join(LOGS_FOLDER, 'server.log')
    ))
    server_logger.setLevel(logging.DEBUG)


def init_app(config_path: str = DEFAULT_CONFIG_PATH) -> web.Application:
    """Application factory."""
    app = web.Application()
    app['config'] = get_config(config_path)

    aiohttp_jinja2.setup(
        app,
        loader=jinja2.FileSystemLoader(
            os.path.join(BASEDIR, 'src', 'templates')
        )
    )
    app['static_root_url'] = '/static'

    setup_routes(app)
    setup_middlewares(app)
    setup_logging()

    app.cleanup_ctx.append(pg_context)

    return app
