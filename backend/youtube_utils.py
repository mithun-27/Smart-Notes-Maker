# backend/youtube_utils.py

import re
from urllib.parse import urlparse, parse_qs

from youtube_transcript_api import (
    YouTubeTranscriptApi,
    TranscriptsDisabled,
    NoTranscriptFound,
    VideoUnavailable,
)

from summarizer import split_into_sentences, normalize_text


def extract_video_id(url: str) -> str | None:
    """
    Extract a YouTube video ID from:
    - https://www.youtube.com/watch?v=VIDEO_ID
    - https://youtu.be/VIDEO_ID
    - https://www.youtube.com/shorts/VIDEO_ID
    - https://www.youtube.com/embed/VIDEO_ID
    - or just the raw VIDEO_ID itself
    """
    if not url:
        return None

    url = url.strip()

    # If it's already a bare video ID (no http, looks like an ID)
    if "http" not in url:
        if re.fullmatch(r"[0-9A-Za-z_-]{6,}", url):
            return url
        return None

    try:
        parsed = urlparse(url)
        host = (parsed.netloc or "").lower()

        # youtu.be short URL
        if "youtu.be" in host:
            vid = parsed.path.lstrip("/")
            return vid or None

        # Normal youtube URLs
        if "youtube.com" in host:
            path = parsed.path or ""

            # Standard watch URL: /watch?v=VIDEO_ID
            if path.startswith("/watch"):
                qs = parse_qs(parsed.query or "")
                if "v" in qs and qs["v"]:
                    return qs["v"][0]

            # Shorts URL: /shorts/VIDEO_ID
            if path.startswith("/shorts/"):
                return path.split("/shorts/")[1].split("/")[0] or None

            # Embed URL: /embed/VIDEO_ID
            if path.startswith("/embed/"):
                return path.split("/embed/")[1].split("/")[0] or None

    except Exception:
        return None

    return None


def fetch_youtube_transcript(url: str) -> str:
    """
    Fetch full transcript text for a YouTube video URL or ID.

    Uses the modern youtube-transcript-api style:

        api = YouTubeTranscriptApi()
        transcript = api.fetch(video_id, languages=['en'])

    Returns:
        A single long string containing the transcript text.

    Raises:
        ValueError with a friendly message if anything goes wrong.
    """
    video_id = extract_video_id(url)
    if not video_id:
        raise ValueError("Invalid YouTube URL or video ID.")

    api = YouTubeTranscriptApi()

    try:
        # Try to fetch an English transcript (can add more language codes if you want)
        fetched = api.fetch(video_id, languages=["en"])
    except TranscriptsDisabled:
        raise ValueError("Transcripts are disabled for this video on YouTube.")
    except NoTranscriptFound:
        raise ValueError("No English transcript was found for this video.")
    except VideoUnavailable:
        raise ValueError("This YouTube video is unavailable.")
    except Exception:
        # Covers weird internal errors, XML issues, IP blocks, etc.
        raise ValueError(
            "Could not fetch transcript for this video. "
            "It may not have an accessible English transcript, "
            "or YouTube is blocking automated requests from your network right now."
        )

    # `fetched` is a FetchedTranscript object. Prefer the official raw API:
    try:
        raw_data = fetched.to_raw_data()
        parts = [
            (item.get("text") or "").replace("\n", " ").strip()
            for item in raw_data
            if item.get("text")
        ]
    except AttributeError:
        # Fallback: iterate over snippets
        parts = []
        for snippet in fetched:
            text = getattr(snippet, "text", "")
            if text:
                parts.append(text.replace("\n", " ").strip())

    transcript_text = " ".join(parts).strip()
    if not transcript_text:
        raise ValueError("Transcript was fetched but contained no text.")

    return clean_transcript_text(transcript_text)


def _too_similar(a: str, b: str, threshold: float = 0.8) -> bool:
    set_a = set(a.lower().split())
    set_b = set(b.lower().split())
    if not set_a or not set_b:
        return False
    overlap = len(set_a & set_b) / len(set_a | set_b)
    return overlap >= threshold


def clean_transcript_text(raw_text: str) -> str:
    """
    Lightly clean a transcript to remove filler intros and repeated lines.
    This keeps summaries from being dominated by greetings/openers.
    """
    filler_start = re.compile(
        r"^(hey|hi|hello|what's up everybody|welcome back|thanks for watching|today i'm going to)",
        re.IGNORECASE,
    )

    sentences = split_into_sentences(raw_text)
    cleaned = []
    for s in sentences:
        s = normalize_text(s)
        if not s:
            continue
        if filler_start.search(s):
            # skip obvious greeting/intro
            continue
        if any(_too_similar(s, prev) for prev in cleaned):
            continue
        cleaned.append(s)

    return " ".join(cleaned) if cleaned else raw_text.strip()
