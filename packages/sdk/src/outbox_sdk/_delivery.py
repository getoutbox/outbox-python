from __future__ import annotations

import hashlib
import hmac
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Mapping

    from outbox_sdk._types import DeliveryEvent

from google.protobuf import message as proto_message
from google.protobuf.json_format import ParseDict
from outbox.v1.destination_pb2 import DeliveryEvent as ProtoDeliveryEvent
from outbox_sdk._mappers import map_delivery_event
from outbox_sdk._types import UnknownDeliveryEvent


def verify(*, body: bytes, secret: str, signature: str) -> bool:
    """Verify a delivery signature using HMAC-SHA256 with timing-safe comparison."""
    expected = hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, signature)


def parse(body: bytes | bytearray | Mapping[str, object]) -> DeliveryEvent:
    """Parse a delivery payload into a typed :class:`DeliveryEvent`.

    Accepts either a proto-binary ``bytes`` payload or a pre-decoded JSON
    ``dict``. Check ``event.type`` to discriminate the variant:

    .. code-block:: python

        event = parse(body)
        if event.type != "message":
            return
        msg = event.message  # typed as Message

    Variants:

    - ``"message"`` → ``event.message: Message``
    - ``"delivery_update"`` → ``event.delivery_update: MessageDelivery``
    - ``"read_receipt"`` → ``event.read_receipt: ReadReceiptEvent``
    - ``"typing_indicator"`` → ``event.typing_indicator: TypingIndicatorEvent``
    - ``"unknown"`` → unrecognised event type
    """
    proto = ProtoDeliveryEvent()
    if isinstance(body, (bytes, bytearray)):
        try:
            proto.ParseFromString(bytes(body))
        except proto_message.DecodeError:
            return UnknownDeliveryEvent(
                connector_id="",
                delivery_id="",
                destination_id="",
                enqueue_time=None,
            )
    else:
        ParseDict(body, proto, ignore_unknown_fields=True)
    return map_delivery_event(proto)


__all__ = [
    "parse",
    "verify",
]
