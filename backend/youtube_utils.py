# backend/youtube_utils.py

import re
from urllib.parse import urlparse, parse_qs
from youtube_transcript_api import YouTubeTranscriptApi

def extract_video_id(url: str) -> str | None:
    """
    Handles URLs like:
    - https://www.youtube.com/watch?v=VIDEO_ID
    - https://youtu.be/VIDEO_ID
    """
    try:
        parsed = urlparse(url)
        if parsed.netloc in ("youtu.be",):
            return parsed.path.lstrip("/")

        if "youtube.com" in parsed.netloc:
            qs = parse_qs(parsed.query)
            return qs.get("v", [None])[0]
    except Exception:
        return None
    return None

def fetch_youtube_transcript(url: str) -> str:
    video_id = extract_video_id(url)
    if not video_id:
        raise ValueError("Could not extract video ID from URL.")

    transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=["en"])
    text = " ".join([t["text"] for t in transcript_list])
    return text
