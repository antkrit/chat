"""Populate database."""
import sys
from sqlalchemy import create_engine
from src.database import sample_data
from src.utils.config import get_config
from src.utils.globals import DB_DSN, DEFAULT_CONFIG_PATH

if __name__ == '__main__':
    config_path = sys.argv[1] if sys.argv[1:] else DEFAULT_CONFIG_PATH
    config = get_config(config_path)

    db_url = DB_DSN.format(**config['postgres'])
    engine = create_engine(db_url)

    sample_data(engine)
