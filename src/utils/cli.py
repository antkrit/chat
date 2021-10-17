import argparse
from src.utils.globals import DEFAULT_CONFIG_PATH

default_parser = argparse.ArgumentParser(description='Get arguments from cli.')
default_parser.add_argument('-c', '--config', default=DEFAULT_CONFIG_PATH,
                            type=str, nargs='?', help='Config path.')
