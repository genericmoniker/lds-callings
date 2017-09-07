import logging
import os

import redis
from rq import Worker, Connection

from application.log import setup_logging, banner
from worker.app import create_app

conn = redis.from_url(os.getenv('REDISTOGO_URL', 'redis://localhost:6379'))

if __name__ == '__main__':
    logger = logging.getLogger()
    setup_logging(logger)
    banner(logger, ' worker ')
    create_app()
    with Connection(conn):
        worker = Worker(['default'])
        worker.work()
