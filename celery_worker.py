# celery_worker.py

"""
Launch this file to start a Celery worker:
    celery -A celery_worker.celery worker --loglevel=info
"""

from app.celery import celery

if __name__ == "__main__":
    # Entrypoint for `python celery_worker.py`
    # But in practice you’d use the celery CLI as shown above.
    celery.worker_main()
