"""Populate database."""
from sqlalchemy import create_engine
from src.database import sample_data
from src.utils.globals import DB_DSN
from src.utils.config import get_config
from src.utils.cli import default_parser

if __name__ == '__main__':
    args = default_parser.parse_args()  # get config path
    config = get_config(args.config)

    db_url = DB_DSN.format(**config['postgres'])
    engine = create_engine(db_url)

    sample_data(engine)
