from __future__ import annotations

import json
from dataclasses import asdict

from openai import OpenAI

from .youtube import Video, discover_videos, transcript


class SummaryError(RuntimeError):
    pass


SYSTEM_PROMPT = """你是嚴謹的影片研究助理。請只根據字幕內容摘要，不補造觀點、數字或價格。
以自然、清楚的繁體中文（台灣用語）輸出 JSON，格式如下：
{"overview":"跨影片總結；單支影片則為核心結論", "videos":[{"video_id":"...","title":"...","summary":"一段摘要","points":["重點1","重點2","重點3"],"takeaway":"一句話結論"}]}
每支影片提供 3–6 個互不重複的具體重點；保留重要數字、時間與不確定語氣。不要提供投資建議。
只輸出合法 JSON，不要 Markdown code fence。"""


def summarize_url(url: str, api_key: str, model: str = "gpt-4.1-mini") -> dict:
    try:
        videos = discover_videos(url, limit=4)
        materials = [_material(video) for video in videos]
    except Exception as exc:
        raise SummaryError(str(exc)) from exc

    client = OpenAI(api_key=api_key)
    try:
        response = client.responses.create(
            model=model,
            instructions=SYSTEM_PROMPT,
            input=json.dumps(materials, ensure_ascii=False),
        )
        result = json.loads(response.output_text)
    except json.JSONDecodeError as exc:
        raise SummaryError("AI 回傳格式無法解析，請再試一次。") from exc
    except Exception as exc:
        raise SummaryError(f"摘要服務呼叫失敗：{exc}") from exc

    by_id = {video.video_id: video for video in videos}
    for item in result.get("videos", []):
        video = by_id.get(item.get("video_id"))
        if video:
            item["url"] = video.url
            item["duration"] = video.duration
            item["upload_date"] = video.upload_date
            item["view_count"] = video.view_count
    result["disclaimer"] = "內容由 AI 根據公開字幕整理，可能有誤；涉及財務資訊時請回看原片並自行查證。"
    return result


def _material(video: Video) -> dict:
    try:
        text = transcript(video.video_id)
    except Exception as exc:
        raise SummaryError(f"〈{video.title}〉無法取得字幕：{exc}") from exc
    data = asdict(video)
    data["transcript"] = text[:90000]
    return data
