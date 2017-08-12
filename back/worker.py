import logging
import os

import redis
from rq import Worker, Connection

from back.log import setup_logging, banner


if __name__ == '__main__':
    logger = logging.getLogger()
    setup_logging(logger)
    banner(logger, ' worker ')
    conn = redis.from_url(os.getenv('REDISTOGO_URL', 'redis://localhost:6379'))
    with Connection(conn):
        worker = Worker(['default'])
        worker.work()
