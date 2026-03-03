import pytest
from outbox_sdk._types import MessagePart, MessagePartDisposition


def test_message_part_text_factory() -> None:
    part = MessagePart.text("hello")
    assert part.content_type == "text/plain"
    assert part.content == b"hello"
    assert part.url is None
    assert part.disposition == MessagePartDisposition.UNSPECIFIED


def test_message_part_text_content_property() -> None:
    part = MessagePart(content_type="text/plain", content=b"world")
    assert part.text_content == "world"


def test_message_part_text_content_raises_when_none() -> None:
    part = MessagePart(content_type="image/jpeg", url="https://example.com/img.jpg")
    with pytest.raises(ValueError, match="no content"):
        _ = part.text_content


def test_message_part_url_part() -> None:
    part = MessagePart(content_type="image/png", url="https://example.com/photo.png")
    assert part.url == "https://example.com/photo.png"
    assert part.content is None


def test_message_part_frozen() -> None:
    part = MessagePart.text("immutable")
    with pytest.raises(Exception):
        part.content_type = "text/html"  # type: ignore[misc]


def test_message_part_text_content_invalid_utf8_raises() -> None:
    """text_content raises UnicodeDecodeError for non-UTF-8 bytes."""
    part = MessagePart(content_type="application/octet-stream", content=b"\xff\xfe")
    with pytest.raises(UnicodeDecodeError):
        _ = part.text_content
