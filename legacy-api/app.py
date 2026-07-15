from __future__ import annotations

import os
import threading
import webbrowser

from flask import Flask, jsonify, render_template, request

from src.summarizer import SummaryError, summarize_url


def create_app() -> Flask:
    app = Flask(__name__)

    @app.get("/")
    def index():
        return render_template("index.html")

    @app.post("/api/summarize")
    def summarize():
        payload = request.get_json(silent=True) or {}
        url = str(payload.get("url", "")).strip()
        api_key = str(payload.get("apiKey", "")).strip() or os.getenv("OPENAI_API_KEY", "")
        if not url:
            return jsonify({"error": "Please paste a YouTube URL."}), 400
        if not api_key:
            return jsonify({"error": "Enter an OpenAI API key or set OPENAI_API_KEY."}), 400
        try:
            result = summarize_url(url, api_key=api_key)
            return jsonify(result)
        except SummaryError as exc:
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
