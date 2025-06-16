# app/config.py
import os
from dotenv import load_dotenv

# Load .env in project root
load_dotenv()

# MongoDB
MONGO_URI: str = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME: str = os.getenv("DB_NAME", "clipo_ai")

# Redis (Celery broker & result backend)
REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")

# File storage (ensure these dirs exist or create them at startup)
VIDEO_STORAGE_PATH: str = os.getenv("VIDEO_STORAGE_PATH", "./storage/videos")
THUMBNAIL_STORAGE_PATH: str = os.getenv("THUMBNAIL_STORAGE_PATH", "./storage/thumbnails")
 