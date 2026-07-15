from unittest.mock import patch

from app import create_app


def test_health():
    client = create_app().test_client()
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}


def test_missing_url():
    client = create_app().test_client()
    response = client.post("/api/summarize", json={"apiKey": "test"})
    assert response.status_code == 400
    assert "網址" in response.get_json()["error"]


def test_missing_api_key(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    client = create_app().test_client()
    response = client.post("/api/summarize", json={"url": "https://youtu.be/abcdefghijk"})
    assert response.status_code == 400
    assert "API Key" in response.get_json()["error"]


@patch("app.summarize_url")
def test_success(mock_summary):
    mock_summary.return_value = {"overview": "總結", "videos": []}
    client = create_app().test_client()
    response = client.post("/api/summarize", json={"url": "https://youtu.be/abcdefghijk", "apiKey": "test"})
    assert response.status_code == 200
    assert response.get_json()["overview"] == "總結"
