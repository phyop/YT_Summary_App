from __future__ import annotations

import re
from dataclasses import dataclass
from urllib.parse import parse_qs, urlparse

import yt_dlp
from youtube_transcript_api import YouTubeTranscriptApi


YOUTUBE_HOSTS = {"youtube.com", "www.youtube.com", "m.youtube.com", "youtu.be"}


@dataclass(frozen=True)
class Video:
    video_id: str
    title: str
    url: str
    duration: int | None = None
    upload_date: str | None = None
    view_count: int | None = None


def validate_youtube_url(url: str) -> None:
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"} or parsed.hostname not in YOUTUBE_HOSTS:
        raise ValueError("Only valid YouTube URLs are supported.")


def video_id_from_url(url: str) -> str | None:
    parsed = urlparse(url)
    if parsed.hostname == "youtu.be":
        candidate = parsed.path.strip("/").split("/")[0]
    else:
        candidate = parse_qs(parsed.query).get("v", [None])[0]
        if not candidate:
            match = re.search(r"/(?:shorts|live|embed)/([\w-]{11})", parsed.path)
            candidate = match.group(1) if match else None
    return candidate if candidate and re.fullmatch(r"[\w-]{11}", candidate) else None


def discover_videos(url: str, limit: int = 4) -> list[Video]:
    validate_youtube_url(url)
    direct_id = video_id_from_url(url)
    if direct_id:
        return [_metadata(url, direct_id)]

    options = {
        "quiet": True,
        "extract_flat": True,
        "playlistend": max(limit * 3, 12),
        "skip_download": True,
        "ignoreerrors": True,
    }
    with yt_dlp.YoutubeDL(options) as ydl:
        info = ydl.extract_info(url, download=False)
    entries = (info or {}).get("entries") or []
    videos: list[Video] = []
    for entry in entries:
        if not entry or entry.get("live_status") in {"is_live", "is_upcoming"}:
            continue
        video_id = entry.get("id")
        title = entry.get("title") or "Untitled video"
        if not video_id or title == "[Private video]":
            continue
        videos.append(
            Video(
                video_id=video_id,
                title=title,
                url=f"https://www.youtube.com/watch?v={video_id}",
                duration=entry.get("duration"),
                upload_date=entry.get("upload_date"),
                view_count=entry.get("view_count"),
            )
        )
        if len(videos) == limit:
            break
    if not videos:
        raise ValueError("No public videos were available for summarization. Check the URL and permissions.")
    return videos


def _metadata(url: str, video_id: str) -> Video:
    options = {"quiet": True, "skip_download": True, "noplaylist": True}
    with yt_dlp.YoutubeDL(options) as ydl:
        info = ydl.extract_info(url, download=False)
    return Video(
        video_id=video_id,
        title=info.get("title") or "Untitled video",
        url=f"https://www.youtube.com/watch?v={video_id}",
        duration=info.get("duration"),
        upload_date=info.get("upload_date"),
        view_count=info.get("view_count"),
    )


def transcript(video_id: str) -> str:
    api = YouTubeTranscriptApi()
    transcript_list = api.list(video_id)
    try:
        selected = transcript_list.find_transcript(["zh-TW", "zh-Hant", "zh", "en"])
    except Exception:
        selected = next(iter(transcript_list))
    snippets = selected.fetch()
    text = " ".join(item.text.replace("\n", " ") for item in snippets)
    if not text.strip():
        raise ValueError("The video does not have a readable transcript.")
    return text
