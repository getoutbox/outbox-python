# packages/sdk/src/outbox_sdk/_types.py
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Literal, TypeAlias

from pydantic import BaseModel, ConfigDict, Field

from outbox_sdk._enums import (
    AccountSource,
    ConnectorKind,
    ConnectorReadiness,
    ConnectorState,
    DestinationEventType,
    DestinationPayloadFormat,
    DestinationState,
    MessageDeletionScope,
    MessageDeliveryStatus,
    MessageDirection,
    MessagePartDisposition,
    TemplateCategory,
    TemplateStatus,
)

_frozen = ConfigDict(frozen=True)

ChannelConfigType: TypeAlias = Literal[
    "activity_pub_bot",
    "activity_pub_user",
    "apple_messages",
    "bluesky_bot",
    "bluesky_user",
    "discord_bot",
    "freshchat",
    "google_chat_bot",
    "google_chat_user",
    "hubspot",
    "in_app",
    "instagram_bot",
    "intercom",
    "kakao_talk_bot",
    "lark_bot",
    "lark_user",
    "line_bot",
    "line_oauth",
    "linkedin_company",
    "linkedin_user",
    "live_chat",
    "matrix_user",
    "mattermost_bot",
    "mattermost_user",
    "messenger_bot",
    "outbox_email",
    "outbox_rcs",
    "outbox_sms",
    "outbox_whatsapp",
    "reddit_bot",
    "reddit_user",
    "signal_user",
    "slack_bot",
    "slack_oauth",
    "teams_bot",
    "telegram_bot",
    "telegram_user",
    "tiktok_bot",
    "tiktok_user",
    "twitch_bot",
    "twitch_user",
    "viber_bot",
    "webex_bot",
    "webex_user",
    "wechat_bot",
    "whatsapp_bot",
    "x_bot",
    "x_user",
    "xmpp_user",
    "zendesk",
    "zoom_chat_s2s",
    "zoom_chat_user",
]

DestinationTargetType: TypeAlias = Literal[
    "webhook",
    "temporal",
    "restate",
    "inngest",
    "cloudflare_worker",
    "golem",
    "hatchet",
    "sqs",
    "sns",
    "event_bridge",
    "kafka",
    "google_pub_sub",
    "nats",
    "smtp",
    "rabbit_mq",
    "azure_service_bus",
    "redis",
]


class Account(BaseModel):
    model_config = _frozen

    id: str
    contact_id: str
    external_id: str
    metadata: dict[str, str]
    source: AccountSource
    create_time: datetime | None = None
    update_time: datetime | None = None


class Connector(BaseModel):
    model_config = _frozen

    id: str
    kind: ConnectorKind = ConnectorKind.UNSPECIFIED
    state: ConnectorState
    readiness: ConnectorReadiness = ConnectorReadiness.UNSPECIFIED
    provisioned_resources: list[str] = Field(default_factory=list)
    webhook_url: str = ""
    display_name: str = ""
    tags: list[str]
    channel_config_type: str | None = None
    channel_config: dict[str, object] | None = None
    # Human-readable error detail when state is ERROR.
    error_message: str | None = None
    create_time: datetime | None = None
    update_time: datetime | None = None


class CreateConnectorResult(BaseModel):
    model_config = _frozen

    connector: Connector
    # Present when the channel requires OAuth authorization.
    # Redirect the user to this URL to complete setup.
    # None for direct-creation channels.
    authorization_url: str | None = None


class ReauthorizeResult(BaseModel):
    model_config = _frozen

    connector: Connector
    authorization_url: str | None = None


class Template(BaseModel):
    model_config = _frozen

    id: str
    connector_id: str
    template_name: str
    language: str
    category: TemplateCategory
    components_json: str
    status: TemplateStatus
    rejection_reason: str = ""
    external_id: str = ""
    create_time: datetime | None = None
    update_time: datetime | None = None


class MessagePart(BaseModel):
    model_config = _frozen

    content_type: str
    disposition: MessagePartDisposition = MessagePartDisposition.UNSPECIFIED
    content: bytes | None = None
    url: str | None = None
    filename: str | None = None

    @classmethod
    def text(cls, text: str) -> MessagePart:
        """Create a text/plain MessagePart from a string."""
        return cls(content_type="text/plain", content=text.encode())

    @property
    def text_content(self) -> str:
        """Decode content bytes to a UTF-8 string. Raises ValueError if content is None."""
        if self.content is None:
            msg = "MessagePart has no content"
            raise ValueError(msg)
        return self.content.decode()


class Message(BaseModel):
    model_config = _frozen

    id: str
    account: Account | None = None
    recipient_id: str
    parts: list[MessagePart]
    metadata: dict[str, str]
    direction: MessageDirection
    deletion_scope: MessageDeletionScope
    edit_number: int
    create_time: datetime | None = None
    deliver_time: datetime | None = None
    delete_time: datetime | None = None
    reply_to_message_id: str | None = None
    group_id: str | None = None
    replaced_message_id: str | None = None


class MessageDelivery(BaseModel):
    model_config = _frozen

    message_id: str
    account: Account | None = None
    status: MessageDeliveryStatus
    error_code: str = ""
    error_message: str = ""
    status_change_time: datetime | None = None


class ReadReceiptEvent(BaseModel):
    model_config = _frozen

    account: Account | None = None
    message_ids: list[str]
    timestamp: datetime | None = None


class TypingIndicatorEvent(BaseModel):
    model_config = _frozen

    account: Account | None = None
    content_type: str | None = None
    timestamp: datetime | None = None
    typing: bool


class Destination(BaseModel):
    model_config = _frozen

    id: str
    display_name: str
    state: DestinationState
    event_types: list[DestinationEventType]
    filter_expression: str
    payload_format: DestinationPayloadFormat
    target_type: DestinationTargetType | None = None
    target_config: dict[str, object] | None = None
    create_time: datetime | None = None
    update_time: datetime | None = None
    last_test_time: datetime | None = None
    last_test_success: bool = False


@dataclass(frozen=True)
class DestinationTestResult:
    success: bool
    error_message: str = ""
    http_status_code: int = 0
    latency_ms: int = 0


@dataclass(frozen=True)
class DestinationTestResultItem:
    success: bool
    error_message: str = ""
    http_status_code: int = 0
    latency_ms: int = 0
    test_time: datetime | None = None


@dataclass(frozen=True)
class ValidateFilterResult:
    valid: bool
    error_message: str = ""
    matched_count: int = 0
    total_count: int = 0


# --- Delivery event discriminated union ---


@dataclass(frozen=True)
class MessageEvent:
    connector_id: str
    delivery_id: str
    destination_id: str
    enqueue_time: datetime | None
    message: Message
    type: Literal["message"] = field(default="message", init=False)


@dataclass(frozen=True)
class DeliveryUpdateEvent:
    connector_id: str
    delivery_id: str
    destination_id: str
    enqueue_time: datetime | None
    delivery_update: MessageDelivery
    type: Literal["delivery_update"] = field(default="delivery_update", init=False)


@dataclass(frozen=True)
class ReadReceiptDeliveryEvent:
    connector_id: str
    delivery_id: str
    destination_id: str
    enqueue_time: datetime | None
    read_receipt: ReadReceiptEvent
    type: Literal["read_receipt"] = field(default="read_receipt", init=False)


@dataclass(frozen=True)
class TypingIndicatorDeliveryEvent:
    connector_id: str
    delivery_id: str
    destination_id: str
    enqueue_time: datetime | None
    typing_indicator: TypingIndicatorEvent
    type: Literal["typing_indicator"] = field(default="typing_indicator", init=False)


@dataclass(frozen=True)
class UnknownDeliveryEvent:
    connector_id: str
    delivery_id: str
    destination_id: str
    enqueue_time: datetime | None
    type: Literal["unknown"] = field(default="unknown", init=False)


DeliveryEvent: TypeAlias = (
    MessageEvent | DeliveryUpdateEvent | ReadReceiptDeliveryEvent | TypingIndicatorDeliveryEvent | UnknownDeliveryEvent
)
