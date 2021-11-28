"""Sources root package.

Initializes web application and web service, contains following subpackages
and modules:

Subpackages:

- `database`: contains everything related to database, including migrations
- `middlewares`: contains modules with request preprocessors/middlewares
- `rest`: contains modules with RESTful service implementation
- `schemas`: contains modules with serialization/deserialization schemas \
for models
- `services`: contains modules with classes used for CRUD operations
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
import aiohttp_debugtoolbar

from aiohttp import web
from src.database import pg_context
from src.views import index, chat
from src.middlewares import error_middleware, add_request_id_middleware
from src.utils.globals import (
    LOGS_FOLDER, DEFAULT_LOGS_FORMAT, DEFAULT_CONFIG_PATH,
    STATIC_FOLDER, TEMPLATES_FOLDER
)
from src.utils.config import get_config
from src.utils.log import setup_log_record_factory, create_log_handler

# fix of an issue: https://github.com/aio-libs/aiopg/issues/678
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

__author__ = 'Anton Krytskyi'
__maintainer__ = __author__

__email__ = 'mujanjagusav@gmail.com'
__license__ = 'MIT'
__version__ = '0.2.1'

__all__ = (
    '__author__',
    '__maintainer__',
    '__email__',
    '__license__',
    '__version__',
)


def setup_routes(app: web.Application) -> None:
    """Add routes to app router."""
    app.router.add_get('/', index, name='index')
    app.router.add_get('/chat/{chat_uuid}', chat, name='chat')
    app.router.add_static(
        '/static/',
        path=STATIC_FOLDER,
        name='static'
    )


def setup_logging() -> None:
    """Configure loggers."""
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
    server_logger.setLevel(logging.ERROR)

    logging.getLogger('faker').setLevel(logging.ERROR)


def init_app(*args, **kwargs) -> web.Application:
    """Application factory.

    Important: first parameter of *args must be config path
    :returns: `web.Application`
    """
    _app = web.Application(middlewares=[
        add_request_id_middleware,
        error_middleware
    ])

    _app['config'] = get_config(args[0] if args else DEFAULT_CONFIG_PATH)
    _app['static_root_url'] = '/static'
    _app['websockets'] = dict()
    _app['session'] = dict()

    setup_routes(_app)
    setup_logging()

    aiohttp_jinja2.setup(
        _app,
        loader=jinja2.FileSystemLoader(
            TEMPLATES_FOLDER
        )
    )
    aiohttp_debugtoolbar.setup(
        _app, enabled=_app['config']['app'].get('debug', False)
    )

    _app.cleanup_ctx.append(pg_context)

    return _app
