from unittest.mock import patch

from app import create_app


def test_health():
    response = create_app().test_client().get("/api/health")
    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}


def test_missing_url():
    response = create_app().test_client().post("/api/summarize", json={})
    assert response.status_code == 400
    assert "YouTube URL" in response.get_json()["error"]


@patch("app.codex_status")
def test_status(mock_status):
    mock_status.return_value = {"installed": True, "loggedIn": True, "message": "Logged in using ChatGPT"}
    response = create_app().test_client().get("/api/status")
    assert response.get_json()["loggedIn"] is True


@patch("app.summarize_with_codex")
@patch("app.transcript", return_value="public transcript")
@patch("app.discover_videos")
def test_success(mock_discover, _mock_transcript, mock_summary):
    from src.youtube import Video

    mock_discover.return_value = [Video("abcdefghijk", "Title", "https://youtu.be/abcdefghijk")]
    mock_summary.return_value = {
        "overview": "Summary",
        "videos": [
            {
                "video_id": "abcdefghijk",
                "title": "Title",
                "summary": "Short summary",
                "points": ["First point", "Second point", "Third point"],
                "takeaway": "Main takeaway",
            }
        ],
    }
    response = create_app().test_client().post("/api/summarize", json={"url": "https://youtu.be/abcdefghijk"})
    assert response.status_code == 200
    assert response.get_json()["overview"] == "Summary"
