from src.utils.globals import FLASH_NEW_REQUEST_KEY, FLASH_OLD_REQUEST_KEY


def flash_set(request, key, value):
    """Save new flash to request."""
    request[FLASH_NEW_REQUEST_KEY][key] = value


def flash_get(request, key, default=None):
    """Get flash from request."""
    return request[FLASH_OLD_REQUEST_KEY].get(key, default)
