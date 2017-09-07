import logging

import sys


def setup_logging(logger):
    handler = logging.StreamHandler(sys.stdout)
    fmt = '%(asctime)s [%(thread)d] %(levelname)1.1s %(message)s'
    formatter = logging.Formatter(fmt)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)


def banner(logger, title):
    logger.info(title.center(25, '='))
