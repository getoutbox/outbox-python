import hashlib
import hmac

from outbox.v1 import destination_pb2, message_pb2
from outbox_sdk._delivery import parse, verify
from outbox_sdk._types import (
    DeliveryUpdateEvent,
    MessageEvent,
    ReadReceiptDeliveryEvent,
    TypingIndicatorDeliveryEvent,
    UnknownDeliveryEvent,
)

# --- verify() tests ---


def test_verify_valid_signature() -> None:
    secret = "mysecret"
    body = b"hello world"
    sig = hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()
    assert verify(body=body, secret=secret, signature=sig) is True


def test_verify_invalid_signature() -> None:
    assert verify(body=b"hello", secret="mysecret", signature="badsig") is False


def test_verify_wrong_secret() -> None:
    body = b"payload"
    sig = hmac.new(b"correct", body, hashlib.sha256).hexdigest()
    assert verify(body=body, secret="wrong", signature=sig) is False


def test_verify_empty_body() -> None:
    secret = "s"
    body = b""
    sig = hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()
    assert verify(body=body, secret=secret, signature=sig) is True


# --- parse() tests: binary proto ---


def _make_message_event_proto() -> bytes:
    proto = destination_pb2.DeliveryEvent()
    proto.connector = "connectors/conn-1"
    proto.message.name = "messages/msg-1"
    proto.message.recipient = "accounts/recip-1"
    proto.message.direction = message_pb2.Message.Direction.DIRECTION_INBOUND
    return proto.SerializeToString()


def test_parse_binary_message_event() -> None:
    body = _make_message_event_proto()
    event = parse(body)
    assert isinstance(event, MessageEvent)
    assert event.type == "message"
    assert event.connector_id == "conn-1"
    assert event.message.id == "msg-1"


def test_parse_binary_delivery_update() -> None:
    proto = destination_pb2.DeliveryEvent()
    proto.connector = "connectors/conn-2"
    proto.delivery_update.message = "messages/msg-2"
    proto.delivery_update.status = message_pb2.MessageDelivery.Status.STATUS_DELIVERED
    body = proto.SerializeToString()

    event = parse(body)
    assert isinstance(event, DeliveryUpdateEvent)
    assert event.type == "delivery_update"
    assert event.delivery_update.message_id == "msg-2"


def test_parse_binary_read_receipt() -> None:
    proto = destination_pb2.DeliveryEvent()
    proto.connector = "connectors/conn-3"
    proto.read_receipt.messages.extend(["messages/msg-3", "messages/msg-4"])
    body = proto.SerializeToString()

    event = parse(body)
    assert isinstance(event, ReadReceiptDeliveryEvent)
    assert event.type == "read_receipt"
    assert event.read_receipt.message_ids == ["msg-3", "msg-4"]


def test_parse_binary_typing_indicator() -> None:
    proto = destination_pb2.DeliveryEvent()
    proto.connector = "connectors/conn-4"
    proto.typing_indicator.typing = True
    body = proto.SerializeToString()

    event = parse(body)
    assert isinstance(event, TypingIndicatorDeliveryEvent)
    assert event.type == "typing_indicator"
    assert event.typing_indicator.typing is True


def test_parse_binary_unknown_event() -> None:
    proto = destination_pb2.DeliveryEvent()
    proto.connector = "connectors/conn-5"
    # No event field set
    body = proto.SerializeToString()

    event = parse(body)
    assert isinstance(event, UnknownDeliveryEvent)
    assert event.type == "unknown"


# --- parse() tests: JSON dict ---


def test_parse_json_message_event() -> None:
    payload = {
        "connector": "connectors/conn-1",
        "message": {
            "name": "messages/msg-1",
            "recipient": "accounts/recip-1",
            "direction": "DIRECTION_OUTBOUND",
        },
    }
    event = parse(payload)
    assert isinstance(event, MessageEvent)
    assert event.type == "message"
    assert event.connector_id == "conn-1"
    assert event.message.id == "msg-1"


def test_parse_json_unknown_fields_ignored() -> None:
    payload = {
        "connector": "connectors/conn-1",
        "unknownField": "value",
        "message": {
            "name": "messages/msg-1",
            "recipient": "accounts/recip-1",
        },
    }
    # Should not raise
    event = parse(payload)
    assert isinstance(event, MessageEvent)


def test_parse_json_delivery_update() -> None:
    payload = {
        "connector": "connectors/conn-1",
        "deliveryUpdate": {
            "message": "messages/msg-5",
            "status": "STATUS_DISPLAYED",
        },
    }
    event = parse(payload)
    assert isinstance(event, DeliveryUpdateEvent)
    assert event.delivery_update.message_id == "msg-5"


def test_parse_empty_binary() -> None:
    event = parse(b"")
    assert isinstance(event, UnknownDeliveryEvent)


def test_verify_sha256_prefixed_signature_fails() -> None:
    """Signature in 'sha256=...' format should fail — raw hex only."""
    secret = "mysecret"
    body = b"hello world"
    raw_sig = hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()
    prefixed = f"sha256={raw_sig}"
    assert verify(body=body, secret=secret, signature=prefixed) is False


def test_verify_empty_signature_fails() -> None:
    """Empty string signature should fail."""
    assert verify(body=b"hello", secret="mysecret", signature="") is False


def test_verify_binary_body() -> None:
    """verify() works with binary (e.g. protobuf) body content."""
    secret = "webhook-secret"
    body = b"\x0a\x04test\x12\x08payload"
    sig = hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()
    assert verify(body=body, secret=secret, signature=sig) is True


def test_verify_case_sensitive_signature() -> None:
    """Hex digest comparison is case-sensitive."""
    secret = "sec"
    body = b"data"
    sig = hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()
    # Flip case of first character
    flipped = sig[0].upper() + sig[1:] if sig[0].islower() else sig[0].lower() + sig[1:]
    assert verify(body=body, secret=secret, signature=flipped) is False


def test_verify_json_body() -> None:
    """verify() works with JSON-encoded body."""
    secret = "api-key"
    body = b'{"event":"message_received","id":"msg-123"}'
    sig = hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()
    assert verify(body=body, secret=secret, signature=sig) is True


def test_parse_malformed_varint_returns_unknown() -> None:
    """Malformed protobuf bytes (invalid varint) return UnknownDeliveryEvent, not raise."""
    event = parse(b"\x80\x80\x80")
    assert isinstance(event, UnknownDeliveryEvent)
    assert event.type == "unknown"
    assert event.connector_id == ""


def test_parse_truncated_proto_returns_unknown() -> None:
    """Truncated proto bytes return UnknownDeliveryEvent, not raise."""
    # Start of a valid proto but cut off mid-field
    event = parse(b"\x0a\x10truncated")
    assert isinstance(event, UnknownDeliveryEvent)
    assert event.type == "unknown"


def test_parse_garbage_bytes_returns_unknown() -> None:
    """Arbitrary garbage bytes return UnknownDeliveryEvent, not raise."""
    event = parse(b"\xff\xfe\xfd\xfc\xfb")
    assert isinstance(event, UnknownDeliveryEvent)
    assert event.type == "unknown"


def test_parse_bytearray_input() -> None:
    """parse() accepts bytearray in addition to bytes."""
    body = bytearray(_make_message_event_proto())
    event = parse(body)
    assert isinstance(event, MessageEvent)
    assert event.connector_id == "conn-1"
