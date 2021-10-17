import logging

from aiohttp.web import run_app
from src import init_app
from src.utils.log import CustomAccessLogger
from src.utils.cli import default_parser

if __name__ == "__main__":
    logger = logging.getLogger('aiohttp')
    args = default_parser.parse_args()  # get config path

    app = init_app(config_path=args.config)
    logger.info("Starting app..")
    run_app(app, access_log_class=CustomAccessLogger)
