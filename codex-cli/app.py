from __future__ import annotations

import threading
import webbrowser

from flask import Flask, jsonify, render_template, request

from src.codex_runner import CodexError, codex_status, summarize_with_codex
from src.youtube import VideoError, discover_videos, transcript


def create_app() -> Flask:
    app = Flask(__name__)

    @app.get("/")
    def index():
        return render_template("index.html")

    @app.get("/api/status")
    def status():
        return jsonify(codex_status())

    @app.post("/api/summarize")
    def summarize():
        payload = request.get_json(silent=True) or {}
        url = str(payload.get("url", "")).strip()
        if not url:
            return jsonify({"error": "Please paste a YouTube URL."}), 400
        try:
            videos = discover_videos(url, limit=4)
            materials = []
            for video in videos:
                item = video.as_dict()
                item["transcript"] = transcript(video.video_id)
                materials.append(item)
            result = summarize_with_codex(materials)
            by_id = {video.video_id: video for video in videos}
            for item in result.get("videos", []):
                video = by_id.get(item.get("video_id"))
                if video:
                    item.update(video.public_metadata())
            result["disclaimer"] = (
                "This summary was generated from public transcript text and may contain errors. "
                "Verify important details against the original video."
            )
            return jsonify(result)
        except (VideoError, CodexError) as exc:
            return jsonify({"error": str(exc)}), 400
        except Exception:
            app.logger.exception("Unexpected summarization error")
            return jsonify({"error": "Unexpected error while processing the video. Please try again."}), 500

    @app.get("/api/health")
    def health():
        return jsonify({"status": "ok"})

    return app


if __name__ == "__main__":
    application = create_app()
    url = "http://127.0.0.1:8765"
    threading.Timer(1.0, lambda: webbrowser.open(url)).start()
    application.run(host="127.0.0.1", port=8765, debug=False)
