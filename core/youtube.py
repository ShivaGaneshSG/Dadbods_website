"""
DadBods YouTube Integration Service.
Fetches actual channel videos dynamically via YouTube Data API v3 when YOUTUBE_API_KEY is provided,
or delivers actual curated DadBods channel videos from https://www.youtube.com/@DADBODS_221.
"""

import os
import urllib.request
import json
import logging
from django.conf import settings
from django.core.cache import cache

logger = logging.getLogger(__name__)

YOUTUBE_CHANNEL_URL = "https://www.youtube.com/@DADBODS_221"
YOUTUBE_CHANNEL_HANDLE = "@DADBODS_221"

# Actual, verified uploads from the official DadBods channel (@DADBODS_221)
VERIFIED_YOUTUBE_VIDEOS = [
    {
        "id": "8ykaCfqJaS8",
        "title": "24 DAYS OUT FROM ICN GOA",
        "url": "https://www.youtube.com/watch?v=8ykaCfqJaS8",
        "thumbnail": "https://i.ytimg.com/vi/8ykaCfqJaS8/hqdefault.jpg",
    },
    {
        "id": "JIjCfWTTGsA",
        "title": "26 Days Out From ICN GOA",
        "url": "https://www.youtube.com/watch?v=JIjCfWTTGsA",
        "thumbnail": "https://i.ytimg.com/vi/JIjCfWTTGsA/hqdefault.jpg",
    },
    {
        "id": "OpoPxxxvl7c",
        "title": "27 Days Out From ICN GOA",
        "url": "https://www.youtube.com/watch?v=OpoPxxxvl7c",
        "thumbnail": "https://i.ytimg.com/vi/OpoPxxxvl7c/hqdefault.jpg",
    },
    {
        "id": "YqbxPQ9aixE",
        "title": "31 Days Out From ICN GOA",
        "url": "https://www.youtube.com/watch?v=YqbxPQ9aixE",
        "thumbnail": "https://i.ytimg.com/vi/YqbxPQ9aixE/hqdefault.jpg",
    },
]


def get_latest_youtube_videos(limit=4):
    """
    Returns recent actual DadBods videos.
    Uses YouTube Data API v3 if YOUTUBE_API_KEY is configured in settings or environment.
    Falls back cleanly to actual verified channel uploads when key is not configured or on network timeout.
    """
    api_key = getattr(settings, "YOUTUBE_API_KEY", "") or os.environ.get("YOUTUBE_API_KEY", "")
    if not api_key:
        return VERIFIED_YOUTUBE_VIDEOS[:limit]

    cache_key = f"dadbods_yt_videos_{limit}"
    cached = cache.get(cache_key)
    if cached:
        return cached

    try:
        url = (
            f"https://www.googleapis.com/youtube/v3/search"
            f"?part=snippet&order=date&type=video&maxResults={limit}"
            f"&q=DADBODS_221&key={api_key}"
        )
        req = urllib.request.Request(url, headers={"User-Agent": "DadBodsPlatform/1.0"})
        with urllib.request.urlopen(req, timeout=3.0) as response:
            payload = json.loads(response.read().decode("utf-8"))
            items = payload.get("items", [])
            videos = []
            for item in items:
                vid_id = item.get("id", {}).get("videoId")
                snippet = item.get("snippet", {})
                if vid_id and snippet:
                    thumbnail = (
                        snippet.get("thumbnails", {}).get("high", {}).get("url")
                        or f"https://i.ytimg.com/vi/{vid_id}/hqdefault.jpg"
                    )
                    videos.append({
                        "id": vid_id,
                        "title": snippet.get("title", "DadBods"),
                        "url": f"https://www.youtube.com/watch?v={vid_id}",
                        "thumbnail": thumbnail,
                    })
            if videos:
                cache.set(cache_key, videos, 3600)
                return videos
    except Exception as e:
        logger.warning(f"Dynamic YouTube API retrieval fallback triggered: {e}")

    return VERIFIED_YOUTUBE_VIDEOS[:limit]
