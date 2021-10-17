import logging
from aiohttp.abc import AbstractAccessLogger
from src.middlewares.log import REQUEST_ID
from src.utils.globals import DEFAULT_LOGS_FORMAT


def setup_log_record_factory():
    """Wrap logging request factory so that [request_id] \
    tag is added to each message."""  # noqa: D401
    old_factory = logging.getLogRecordFactory()

    def new_factory(*args, **kwargs):
        record = old_factory(*args, **kwargs)
        req_id = REQUEST_ID.get(None)
        record.request_id_prefix = f'[{req_id}] ' if req_id else ''
        return record

    logging.setLogRecordFactory(new_factory)


def create_log_handler(handler, output,
                       format_str=DEFAULT_LOGS_FORMAT, level=logging.DEBUG):
    """Create logging handler with given parameters."""
    custom_handler = handler(output)
    custom_handler.setFormatter(logging.Formatter(format_str))
    custom_handler.setLevel(level)

    return custom_handler


class CustomAccessLogger(AbstractAccessLogger):
    """Realization of :class:`aiohttp.abc.AbstractAccessLogger`.

    Adds FileHandler to logger handlers. Also sets and resets
    request_id tokens (request_id_prefix in format string)
    """

    def log(self, request, response, time):
        """Make log request records. Sets and resets request_id tokens."""
        token = REQUEST_ID.set(request['request_id'])
        try:
            self.logger.info(f'{request.remote} '
                             f'"{request.method} {request.path} '
                             f'done in {time}s. Status: {response.status}')
        finally:
            REQUEST_ID.reset(token)
