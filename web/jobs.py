import os
import redis
from rq.decorators import job

from worker.sync import synchronize

conn = redis.from_url(os.getenv('REDISTOGO_URL', 'redis://localhost:6379'))


@job('default', connection=conn)
def synchronize_async(s, unit):
    synchronize(s, unit)
