import pytest

from src.youtube import validate_youtube_url, video_id_from_url


@pytest.mark.parametrize("url, expected", [
    ("https://www.youtube.com/watch?v=sigSZCnSa6M", "sigSZCnSa6M"),
    ("https://youtu.be/sigSZCnSa6M", "sigSZCnSa6M"),
    ("https://www.youtube.com/shorts/sigSZCnSa6M", "sigSZCnSa6M"),
])
def test_video_id_from_url(url, expected):
    assert video_id_from_url(url) == expected


def test_reject_non_youtube_url():
    with pytest.raises(ValueError):
        validate_youtube_url("https://example.com/video")
