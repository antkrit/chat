from aiohttp.web import run_app
from src import app
from src.utils.log import CustomAccessLogger

if __name__ == "__main__":
    app.logger.info("Starting app..")
    run_app(app, access_log_class=CustomAccessLogger)
