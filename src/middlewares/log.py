import secrets
from asyncio import CancelledError
from aiohttp import web
from contextvars import ContextVar


# context var that contains given request tracing id
REQUEST_ID = ContextVar('request_id')


@web.middleware
async def add_request_id_middleware(request, handler):
    """Set request_id context var and request['request_id'] to \
    some random value."""
    random_req_id = secrets.token_urlsafe(nbytes=6)  # 1 byte ~ 1.3 characters
    request['request_id'] = random_req_id
    token = REQUEST_ID.set(random_req_id)
    try:
        return await handler(request)
    except CancelledError as e:
        # logger.info('(Cancelled)')
        raise e
    finally:
        REQUEST_ID.reset(token)
