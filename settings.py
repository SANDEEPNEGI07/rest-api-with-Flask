"""
settings.py is a setup for rq worker so that we can run this file in render.com when deploy.
In render.com background worker is not free.

"""

import os
from dotenv import load_dotenv

load_dotenv()

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
QUEUES = ["emails", "default"]