from __future__ import annotations

from enum import IntEnum


class ConnectorState(IntEnum):
    UNSPECIFIED = 0
    ACTIVE = 1
    INACTIVE = 2
    AUTHORIZING = 3
    ERROR = 4


class AccountSource(IntEnum):
    UNSPECIFIED = 0
    API = 1
    AUTO = 2


class MessagePartDisposition(IntEnum):
    UNSPECIFIED = 0
    RENDER = 1
    REACTION = 2
    ATTACHMENT = 3
    INLINE = 4


class MessageDirection(IntEnum):
    UNSPECIFIED = 0
    INBOUND = 1
    OUTBOUND = 2


class MessageDeletionScope(IntEnum):
    UNSPECIFIED = 0
    FOR_SENDER = 1
    FOR_EVERYONE = 2


class MessageDeliveryStatus(IntEnum):
    UNSPECIFIED = 0
    PENDING = 1
    DELIVERED = 2
    DISPLAYED = 3
    PROCESSED = 4
    FAILED = 5
    EXPIRED = 6


class DestinationState(IntEnum):
    UNSPECIFIED = 0
    ACTIVE = 1
    PAUSED = 2
    DEGRADED = 3


class DestinationEventType(IntEnum):
    UNSPECIFIED = 0
    MESSAGE = 1
    DELIVERY_UPDATE = 2
    READ_RECEIPT = 3
    TYPING_INDICATOR = 4


class DestinationPayloadFormat(IntEnum):
    UNSPECIFIED = 0
    JSON = 1
    PROTO_BINARY = 2
