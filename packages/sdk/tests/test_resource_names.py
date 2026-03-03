import pytest
from outbox_sdk._resource_names import (
    account_name,
    connector_name,
    destination_name,
    message_name,
    parse_id,
)


def test_connector_name() -> None:
    assert connector_name("abc") == "connectors/abc"


def test_message_name() -> None:
    assert message_name("xyz") == "messages/xyz"


def test_account_name() -> None:
    assert account_name("xyz") == "accounts/xyz"


def test_destination_name() -> None:
    assert destination_name("d1") == "destinations/d1"


def test_parse_id() -> None:
    assert parse_id("connectors/abc") == "abc"
    assert parse_id("channels/whatsapp") == "whatsapp"
    assert parse_id("messages/xyz") == "xyz"
    assert parse_id("accounts/xyz") == "xyz"


def test_parse_id_invalid() -> None:
    with pytest.raises(ValueError, match="Invalid resource name"):
        parse_id("")


def test_parse_id_no_slash_returns_input() -> None:
    """A bare ID with no slash is itself the last segment."""
    assert parse_id("abc") == "abc"


def test_parse_id_trailing_slash_raises() -> None:
    """A resource name ending with '/' has an empty last segment — invalid."""
    with pytest.raises(ValueError, match="Invalid resource name"):
        parse_id("connectors/")


def test_parse_id_multiple_slashes_returns_last_segment() -> None:
    """Only the last segment is returned when there are multiple slashes."""
    assert parse_id("projects/my-project/connectors/conn-1") == "conn-1"
