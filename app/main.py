
import os
from fastapi import FastAPI
from .config import VIDEO_STORAGE_PATH, THUMBNAIL_STORAGE_PATH
from .routers.videos import router as videos_router

os.makedirs(VIDEO_STORAGE_PATH, exist_ok=True)
os.makedirs(THUMBNAIL_STORAGE_PATH, exist_ok=True)

app = FastAPI(title="Clipo AI Backend")

@app.on_event("startup")
def startup_event():
    
    os.makedirs(VIDEO_STORAGE_PATH, exist_ok=True)
    os.makedirs(THUMBNAIL_STORAGE_PATH, exist_ok=True)

    

 
app.include_router(videos_router, prefix="/api")

 
from fastapi.staticfiles import StaticFiles
app.mount("/thumbnails", StaticFiles(directory=THUMBNAIL_STORAGE_PATH), name="thumbnails")
