import sys
import logging

from aiohttp.web import run_app
from src import init_app
from src.utils.log import CustomAccessLogger


def main():
    app = init_app(*sys.argv[1:])
    logging.getLogger('aiohttp').info("Starting app..")
    run_app(app, access_log_class=CustomAccessLogger)


if __name__ == "__main__":
    main()
