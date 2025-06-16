# app/celery.py

from celery import Celery
from .config import REDIS_URL

celery = Celery(
    "clipo_ai",
    broker=REDIS_URL,
    backend=REDIS_URL,
)

# auto-discover tasks in app/tasks.py
celery.autodiscover_tasks(["app.tasks"])
