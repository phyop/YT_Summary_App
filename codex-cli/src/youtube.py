from __future__ import annotations

import re
from dataclasses import dataclass
from urllib.parse import parse_qs, urlparse

import yt_dlp
from youtube_transcript_api import YouTubeTranscriptApi


YOUTUBE_HOSTS = {"youtube.com", "www.youtube.com", "m.youtube.com", "youtu.be"}


class VideoError(RuntimeError):
    pass


@dataclass(frozen=True)
class Video:
    video_id: str
    title: str
    url: str
    duration: int | None = None
    upload_date: str | None = None
    view_count: int | None = None

    def as_dict(self) -> dict:
        return {"video_id": self.video_id, "title": self.title, "url": self.url}

    def public_metadata(self) -> dict:
        return {
            "url": self.url,
            "duration": self.duration,
            "upload_date": self.upload_date,
            "view_count": self.view_count,
        }


def validate_youtube_url(url: str) -> None:
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"} or parsed.hostname not in YOUTUBE_HOSTS:
        raise VideoError("Only valid YouTube URLs are supported.")


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
    options = {
        "quiet": True,
        "skip_download": True,
        "ignoreerrors": True,
        "js_runtimes": {"node": {}},
    }
    if direct_id:
        options["noplaylist"] = True
        with yt_dlp.YoutubeDL(options) as ydl:
            info = ydl.extract_info(url, download=False)
        if not info:
            raise VideoError("No public video was available for summarization.")
        return [_from_info(info, direct_id)]

    options.update({"extract_flat": True, "playlistend": max(limit * 3, 12)})
    with yt_dlp.YoutubeDL(options) as ydl:
        info = ydl.extract_info(url, download=False)
    videos: list[Video] = []
    for entry in (info or {}).get("entries") or []:
        if not entry or entry.get("live_status") in {"is_live", "is_upcoming"}:
            continue
        video_id = entry.get("id")
        title = entry.get("title") or "Untitled video"
        if not video_id or title == "[Private video]":
            continue
        videos.append(_from_info(entry, video_id))
        if len(videos) == limit:
            break
    if not videos:
        raise VideoError("No public videos were available for summarization. Check the URL and permissions.")
    return videos


def _from_info(info: dict, video_id: str) -> Video:
    return Video(
        video_id,
        info.get("title") or "Untitled video",
        f"https://www.youtube.com/watch?v={video_id}",
        info.get("duration"),
        info.get("upload_date"),
        info.get("view_count"),
    )


def transcript(video_id: str) -> str:
    try:
        transcript_list = YouTubeTranscriptApi().list(video_id)
        try:
            selected = transcript_list.find_transcript(["zh-TW", "zh-Hant", "zh", "en"])
        except Exception:
            selected = next(iter(transcript_list))
        text = " ".join(item.text.replace("\n", " ") for item in selected.fetch())
    except Exception as exc:
        raise VideoError(f"Video {video_id} does not have a readable public transcript: {exc}") from exc
    if not text.strip():
        raise VideoError(f"Video {video_id} does not have a readable transcript.")
    return text[:90000]
