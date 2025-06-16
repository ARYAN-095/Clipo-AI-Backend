 

import subprocess
import os
from datetime import timedelta
from typing import Tuple

def extract_duration(video_path: str) -> str:
    """
    Use ffprobe to extract the total duration of a video file.
    Returns a string in "HH:MM:SS" format.
    """
   
    cmd = [
        "ffprobe",
        "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        video_path
    ]

   
    output = subprocess.check_output(cmd, stderr=subprocess.STDOUT).decode().strip()
    total_seconds = float(output)

    
    td = timedelta(seconds=int(total_seconds))
    # datetime.timedelta.__str__ already formats as "D days, HH:MM:SS" if days >0,
    # but most videos are shorter than 24h, so we can directly use str(td)
    return str(td)

def generate_thumbnail(
    video_path: str,
    duration: str,
    storage_path: str,
    percent: float = 0.1
) -> str:
    """
    Generate a thumbnail at the given percentage (default 10%) of the video's duration.
    Saves the thumbnail JPEG under storage_path and returns the thumbnail filename.
    """
     
    h, m, s = map(int, duration.split(":"))
    total_seconds = h * 3600 + m * 60 + s
    
    ts_seconds = int(total_seconds * percent)

     
    os.makedirs(storage_path, exist_ok=True)

     
    base_name = os.path.splitext(os.path.basename(video_path))[0]
    thumb_name = f"{base_name}.jpg"
    thumb_path = os.path.join(storage_path, thumb_name)

     
    cmd = [
        "ffmpeg",
        "-ss", str(ts_seconds),         # seek to timestamp
        "-i", video_path,               # input file
        "-vframes", "1",                # capture exactly one frame
        "-q:v", "2",                    # quality level (lower is better)
        thumb_path
    ]

     
    subprocess.check_call(cmd, stderr=subprocess.STDOUT)

    return thumb_name
