import logging

import sys


def setup_logging(app):
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('%(asctime)s %(levelname)1.1s %(message)s')
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.INFO)
