 
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from bson import ObjectId
from datetime import datetime
import shutil
from ..db import videos_collection
from ..config import VIDEO_STORAGE_PATH
from ..tasks import process_video

router = APIRouter()

@router.post("/upload-video/")
async def upload_video(file: UploadFile = File(...)):
    # 1) Save locally
    file_path = f"{VIDEO_STORAGE_PATH}/{file.filename}"
    with open(file_path, "wb") as dest:
        shutil.copyfileobj(file.file, dest)

    # 2) Insert MongoDB record
    record = {
        "filename": file.filename,
        "upload_time": datetime.utcnow(),
        "status": "pending"
    }
    result = videos_collection.insert_one(record)
    vid = str(result.inserted_id)

    # 3) Trigger Celery task
    process_video.delay(vid)

    return JSONResponse({"id": vid})


@router.get("/video-status/{id}")
def video_status(id: str):
    rec = videos_collection.find_one({"_id": ObjectId(id)})
    if not rec:
        raise HTTPException(404, "Video not found")
    return {"status": rec.get("status", "unknown")}


@router.get("/video-metadata/{id}")
def video_metadata(id: str):
    rec = videos_collection.find_one({"_id": ObjectId(id)})
    if not rec:
        raise HTTPException(404, "Video not found")
    # Convert ObjectId to string and datetime to ISO
    rec["id"] = str(rec["_id"])
    rec["upload_time"] = rec["upload_time"].isoformat()
    rec.pop("_id")
    return rec
