"""Populate database."""
import sys
from src.database import sample_data
from src.utils.config import get_config
from src.utils.globals import DEFAULT_CONFIG_PATH

if __name__ == '__main__':
    config_path = sys.argv[1] if sys.argv[1:] else DEFAULT_CONFIG_PATH
    config = get_config(config_path)

    sample_data(config=config['postgres'])
