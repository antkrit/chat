"""Defines preprocessor to handle browser errors.

Expected errors:
- 404
- 500
"""
import http
import logging
import aiohttp_jinja2
from aiohttp import web
from typing import Callable


logger = logging.getLogger('aiohttp.server')


async def handle_404(request):
    """Return 404 template."""
    return aiohttp_jinja2.render_template(
        'errors/404.html',
        request, {},
        status=404
    )


async def handle_500(request):
    """Return 500 template."""
    return aiohttp_jinja2.render_template(
        'errors/500.html',
        request, {},
        status=500
    )


def create_error_middleware(overrides: dict[int, Callable]):
    """Wrap error_middleware so that each error from 'overrides' can be handled \
    by single function.

    :param overrides: dict where key is error code and value is handler
    :returns: error middleware
    """
    @web.middleware
    async def err_middleware(request, handler):
        try:
            return await handler(request)
        except web.HTTPException as err:
            override = overrides.get(err.status)
            if override:
                if err.status == http.HTTPStatus.INTERNAL_SERVER_ERROR:
                    logger.error('Error occurred.', exc_info=True)
                return await override(request)

            raise
        except Exception:
            logger.error('Unexpected error.', exc_info=True)
            return await overrides[500](request)

    return err_middleware


error_middleware = create_error_middleware({
    404: handle_404,
    500: handle_500
})
