 

from bson import ObjectId
from datetime import datetime
from pymongo import MongoClient

from app.celery import celery
from app.config import MONGO_URI, DB_NAME, VIDEO_STORAGE_PATH, THUMBNAIL_STORAGE_PATH
from app.services.ffmpeg_utils import extract_duration, generate_thumbnail

 
_client = MongoClient(MONGO_URI)
_db = _client[DB_NAME]
videos_collection = _db.videos

@celery.task(name="app.tasks.process_video")
def process_video(video_id: str):
    """
    Background task to:
      - extract duration via FFmpeg
      - generate a thumbnail at 10% of the video
      - update MongoDB record with duration, thumbnail_url, status
    """
     
    rec = videos_collection.find_one({"_id": ObjectId(video_id)})
    if not rec:
        return 

    filename = rec["filename"]
    video_path = f"{VIDEO_STORAGE_PATH}/{filename}"

    
    duration_str = extract_duration(video_path)

     
    thumb_filename = generate_thumbnail(
        video_path=video_path,
        duration=duration_str,
        storage_path=THUMBNAIL_STORAGE_PATH
    )
    thumb_url = f"/thumbnails/{thumb_filename}"

    
    videos_collection.update_one(
        {"_id": ObjectId(video_id)},
        {
            "$set": {
                "duration": duration_str,
                "thumbnail_url": thumb_url,
                "status": "done",
                "processed_time": datetime.utcnow()
            }
        }
    )
