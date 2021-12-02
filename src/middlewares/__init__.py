# flake8: noqa F401
"""This package contains modules with request preprocessors.

Modules:
- `errors.py`: defines preprocessor to handle browser errors (404, 500)
- `flash.py`: defines preprocessor to set flash messages to session
- `request.py`: defines preprocessor to set request tracing id
"""
from src.middlewares.errors import error_middleware
from src.middlewares.flash import flash_middleware
from src.middlewares.request import add_request_id_middleware
