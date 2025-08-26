from __future__ import annotations

import os
from celery import Celery

broker_url = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
backend_url = broker_url

app = Celery('quanticx', broker=broker_url, backend=backend_url)

@app.task
def add(x: int, y: int) -> int:
    return x + y

