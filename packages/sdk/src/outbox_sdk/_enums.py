from __future__ import annotations

from enum import IntEnum


class ConnectorState(IntEnum):
    UNSPECIFIED = 0
    ACTIVE = 1
    INACTIVE = 2
    AUTHORIZING = 3
    ERROR = 4


class ConnectorKind(IntEnum):
    UNSPECIFIED = 0
    MANAGED = 1
    USER = 2
    BOT = 3


class ConnectorReadiness(IntEnum):
    UNSPECIFIED = 0
    READY = 1
    PENDING_COMPLIANCE = 2
    RESOURCE_NOT_ACTIVE = 3
    RESOURCE_SUSPENDED = 4


class ProvisionedResourceState(IntEnum):
    """State of a provisioned resource on a connector.

    Exported for API schema completeness. Individual resource states are not
    currently surfaced by any SDK method return type.
    """

    UNSPECIFIED = 0
    PENDING = 1
    PROVISIONING = 2
    ACTIVE = 3
    SUSPENDED = 4
    RELEASED = 5
    FAILED = 6
    CANCELLING = 7
    PORTING = 8
    PORT_FAILED = 9


class TemplateStatus(IntEnum):
    UNSPECIFIED = 0
    PENDING = 1
    APPROVED = 2
    REJECTED = 3
    PAUSED = 4
    DISABLED = 5


class TemplateCategory(IntEnum):
    UNSPECIFIED = 0
    UTILITY = 1
    MARKETING = 2
    AUTHENTICATION = 3


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
