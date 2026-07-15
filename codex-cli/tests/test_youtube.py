import pytest
from src.youtube import VideoError, validate_youtube_url, video_id_from_url


@pytest.mark.parametrize("url", ["https://www.youtube.com/watch?v=sigSZCnSa6M", "https://youtu.be/sigSZCnSa6M", "https://www.youtube.com/shorts/sigSZCnSa6M"])
def test_video_id(url):
    assert video_id_from_url(url) == "sigSZCnSa6M"


def test_reject_non_youtube():
    with pytest.raises(VideoError):
        validate_youtube_url("https://example.com/video")
