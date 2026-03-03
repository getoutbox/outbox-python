from datetime import UTC, datetime

import pytest
from google.protobuf.timestamp_pb2 import Timestamp
from outbox.v1 import connector_pb2, destination_pb2, message_pb2, template_pb2
from outbox_sdk._enums import (
    AccountSource,
    ConnectorKind,
    ConnectorReadiness,
    ConnectorState,
    DestinationEventType,
    DestinationPayloadFormat,
    DestinationState,
    MessageDeliveryStatus,
    MessageDirection,
    MessagePartDisposition,
    TemplateCategory,
    TemplateStatus,
)
from outbox_sdk._mappers import (
    map_account,
    map_connector,
    map_delivery_event,
    map_destination,
    map_message,
    map_message_delivery,
    map_message_part,
    map_read_receipt,
    map_template,
    map_typing_indicator,
)


def _ts(seconds: int) -> Timestamp:
    t = Timestamp()
    t.seconds = seconds
    t.nanos = 0
    return t


def test_map_connector_basic() -> None:
    proto = connector_pb2.Connector()
    proto.name = "connectors/abc"
    proto.whatsapp_bot.app_id = "app123"
    proto.whatsapp_bot.app_secret = "secret456"
    proto.state = connector_pb2.ConnectorState.CONNECTOR_STATE_ACTIVE
    proto.kind = connector_pb2.ConnectorKind.CONNECTOR_KIND_BOT
    proto.readiness = connector_pb2.ConnectorReadiness.CONNECTOR_READINESS_READY
    proto.display_name = "My WhatsApp Bot"
    proto.webhook_url = "https://example.com/hook"
    proto.create_time.CopyFrom(_ts(1700000000))

    result = map_connector(proto)

    assert result.id == "abc"
    assert result.state == ConnectorState.ACTIVE
    assert result.kind == ConnectorKind.BOT
    assert result.readiness == ConnectorReadiness.READY
    assert result.display_name == "My WhatsApp Bot"
    assert result.webhook_url == "https://example.com/hook"
    assert result.channel_config_type == "whatsapp_bot"
    assert result.channel_config is not None
    assert result.channel_config["app_id"] == "app123"
    assert result.channel_config["app_secret"] == "secret456"
    assert result.create_time == datetime(2023, 11, 14, 22, 13, 20, tzinfo=UTC)


def test_map_connector_error_message() -> None:
    proto = connector_pb2.Connector()
    proto.name = "connectors/abc"
    proto.state = connector_pb2.ConnectorState.CONNECTOR_STATE_ERROR
    proto.error_message = "token expired"

    result = map_connector(proto)

    assert result.state == ConnectorState.ERROR
    assert result.error_message == "token expired"


def test_map_connector_no_channel_config() -> None:
    proto = connector_pb2.Connector()
    proto.name = "connectors/xyz"
    proto.state = connector_pb2.ConnectorState.CONNECTOR_STATE_INACTIVE

    result = map_connector(proto)

    assert result.channel_config_type is None
    assert result.channel_config is None


def test_map_connector_provisioned_resources() -> None:
    proto = connector_pb2.Connector()
    proto.name = "connectors/abc"
    proto.state = connector_pb2.ConnectorState.CONNECTOR_STATE_ACTIVE
    proto.provisioned_resources.extend(
        [
            "provisioned_resources/res-1",
            "provisioned_resources/res-2",
        ]
    )

    result = map_connector(proto)

    assert result.provisioned_resources == ["res-1", "res-2"]


def test_map_message_part_content() -> None:
    proto = message_pb2.MessagePart()
    proto.content_type = "text/plain"
    proto.content = b"Hello"
    proto.disposition = message_pb2.MessagePart.Disposition.DISPOSITION_RENDER

    result = map_message_part(proto)

    assert result.content_type == "text/plain"
    assert result.content == b"Hello"
    assert result.url is None
    assert result.disposition == MessagePartDisposition.RENDER


def test_map_message_part_url() -> None:
    proto = message_pb2.MessagePart()
    proto.content_type = "image/jpeg"
    proto.url = "https://example.com/img.jpg"

    result = map_message_part(proto)

    assert result.url == "https://example.com/img.jpg"
    assert result.content is None


def test_map_message_top_level() -> None:
    """Message.name is now top-level (messages/xyz), no connector_id on result."""
    proto = message_pb2.Message()
    proto.name = "messages/xyz"
    proto.recipient = "accounts/recip-id"
    proto.direction = message_pb2.Message.Direction.DIRECTION_INBOUND

    proto.account.name = "accounts/sender-id"
    proto.account.contact_id = "contact-1"
    proto.account.external_id = "+1234567890"

    result = map_message(proto)

    assert result.id == "xyz"
    assert not hasattr(result, "connector_id")
    assert result.recipient_id == "recip-id"
    assert result.direction == MessageDirection.INBOUND
    assert result.account is not None
    assert result.account.id == "sender-id"
    assert result.account.contact_id == "contact-1"


def test_map_message_delivery_no_channel_id() -> None:
    """MessageDelivery has no channel_id field."""
    proto = message_pb2.MessageDelivery()
    proto.message = "messages/xyz"
    proto.status = message_pb2.MessageDelivery.Status.STATUS_DELIVERED

    result = map_message_delivery(proto)

    assert result.message_id == "xyz"
    assert not hasattr(result, "channel_id")
    assert result.status == MessageDeliveryStatus.DELIVERED


def test_map_destination_typed_enums() -> None:
    proto = destination_pb2.Destination()
    proto.name = "destinations/d1"
    proto.display_name = "My Destination"
    proto.state = destination_pb2.Destination.State.STATE_ACTIVE
    proto.event_types.append(destination_pb2.Destination.EventType.EVENT_TYPE_MESSAGE)
    proto.payload_format = destination_pb2.Destination.PayloadFormat.PAYLOAD_FORMAT_JSON

    result = map_destination(proto)

    assert result.id == "d1"
    assert isinstance(result.state, DestinationState)
    assert result.state == DestinationState.ACTIVE
    assert isinstance(result.event_types[0], DestinationEventType)
    assert result.event_types[0] == DestinationEventType.MESSAGE
    assert isinstance(result.payload_format, DestinationPayloadFormat)
    assert result.payload_format == DestinationPayloadFormat.JSON


def test_map_destination_webhook_target() -> None:
    proto = destination_pb2.Destination()
    proto.name = "destinations/d2"
    proto.display_name = "Webhook"
    proto.webhook.url = "https://example.com/hook"
    proto.webhook.signing_secret = "s3cr3t"

    result = map_destination(proto)

    assert result.target_type == "webhook"
    assert result.target_config is not None
    assert result.target_config["url"] == "https://example.com/hook"
    assert result.target_config["signing_secret"] == "s3cr3t"


def test_map_destination_no_target() -> None:
    proto = destination_pb2.Destination()
    proto.name = "destinations/d3"
    proto.display_name = "No Target"

    result = map_destination(proto)

    assert result.target_type is None
    assert result.target_config is None


def test_map_account_basic() -> None:
    proto = message_pb2.Message().account.__class__()
    # Use the account_pb2 directly
    from outbox.v1 import account_pb2

    proto = account_pb2.Account()
    proto.name = "accounts/acc-1"
    proto.contact_id = "contact-abc"
    proto.external_id = "+15551234567"
    proto.source = account_pb2.Account.Source.SOURCE_API
    proto.metadata["key"] = "value"
    proto.create_time.CopyFrom(_ts(1700000000))
    proto.update_time.CopyFrom(_ts(1700000001))

    result = map_account(proto)

    assert result.id == "acc-1"
    assert result.contact_id == "contact-abc"
    assert result.external_id == "+15551234567"
    assert result.source == AccountSource.API
    assert result.metadata == {"key": "value"}
    assert result.create_time == datetime(2023, 11, 14, 22, 13, 20, tzinfo=UTC)
    assert result.update_time is not None


def test_map_account_no_timestamps() -> None:
    from outbox.v1 import account_pb2

    proto = account_pb2.Account()
    proto.name = "accounts/acc-2"
    proto.contact_id = "contact-xyz"
    proto.external_id = "ext-id"

    result = map_account(proto)

    assert result.id == "acc-2"
    assert result.create_time is None
    assert result.update_time is None


def test_map_read_receipt_basic() -> None:
    from outbox.v1 import message_pb2 as m

    proto = m.ReadReceiptEvent()
    proto.account.name = "accounts/acc-1"
    proto.account.contact_id = "contact-1"
    proto.account.external_id = "ext-1"
    proto.messages.extend(["messages/msg-1", "messages/msg-2"])
    proto.timestamp.CopyFrom(_ts(1700000000))

    result = map_read_receipt(proto)

    assert result.account is not None
    assert result.account.id == "acc-1"
    assert result.message_ids == ["msg-1", "msg-2"]
    assert result.timestamp is not None


def test_map_read_receipt_no_account() -> None:
    from outbox.v1 import message_pb2 as m

    proto = m.ReadReceiptEvent()
    proto.messages.extend(["messages/msg-1"])

    result = map_read_receipt(proto)

    assert result.account is None
    assert result.message_ids == ["msg-1"]


def test_map_typing_indicator_typing_true() -> None:
    from outbox.v1 import message_pb2 as m

    proto = m.TypingIndicatorEvent()
    proto.account.name = "accounts/acc-1"
    proto.account.contact_id = "c"
    proto.account.external_id = "e"
    proto.typing = True
    proto.content_type = "text/plain"
    proto.timestamp.CopyFrom(_ts(1700000000))

    result = map_typing_indicator(proto)

    assert result.account is not None
    assert result.typing is True
    assert result.content_type == "text/plain"
    assert result.timestamp is not None


def test_map_typing_indicator_no_content_type() -> None:
    from outbox.v1 import message_pb2 as m

    proto = m.TypingIndicatorEvent()
    proto.typing = False

    result = map_typing_indicator(proto)

    assert result.typing is False
    assert result.content_type is None
    assert result.account is None


def test_map_delivery_event_message() -> None:
    from outbox.v1 import destination_pb2 as d

    proto = d.DeliveryEvent()
    proto.connector = "connectors/conn-1"
    proto.destination = "destinations/dest-1"
    proto.delivery_id = "dlv-abc"
    proto.message.name = "messages/msg-1"
    proto.message.recipient = "accounts/recip-1"
    proto.message.direction = message_pb2.Message.Direction.DIRECTION_OUTBOUND

    result = map_delivery_event(proto)

    assert result.type == "message"
    assert result.connector_id == "conn-1"
    assert result.destination_id == "dest-1"
    assert result.delivery_id == "dlv-abc"
    assert result.enqueue_time is None  # no enqueue_time set
    assert result.message.id == "msg-1"


def test_map_delivery_event_delivery_update() -> None:
    from outbox.v1 import destination_pb2 as d

    proto = d.DeliveryEvent()
    proto.connector = "connectors/conn-1"
    proto.delivery_update.message = "messages/msg-2"
    proto.delivery_update.status = message_pb2.MessageDelivery.Status.STATUS_DELIVERED

    result = map_delivery_event(proto)

    assert result.type == "delivery_update"
    assert result.connector_id == "conn-1"
    assert result.delivery_update.message_id == "msg-2"
    assert result.delivery_update.status == MessageDeliveryStatus.DELIVERED


def test_map_delivery_event_read_receipt() -> None:
    from outbox.v1 import destination_pb2 as d

    proto = d.DeliveryEvent()
    proto.connector = "connectors/conn-1"
    proto.read_receipt.messages.extend(["messages/msg-1"])

    result = map_delivery_event(proto)

    assert result.type == "read_receipt"
    assert result.read_receipt.message_ids == ["msg-1"]


def test_map_delivery_event_typing_indicator() -> None:
    from outbox.v1 import destination_pb2 as d

    proto = d.DeliveryEvent()
    proto.connector = "connectors/conn-1"
    proto.typing_indicator.typing = True

    result = map_delivery_event(proto)

    assert result.type == "typing_indicator"
    assert result.typing_indicator.typing is True


def test_map_delivery_event_unknown() -> None:
    from outbox.v1 import destination_pb2 as d

    proto = d.DeliveryEvent()
    proto.connector = "connectors/conn-1"
    # No event set → unknown

    result = map_delivery_event(proto)

    assert result.type == "unknown"
    assert result.connector_id == "conn-1"


def test_map_delivery_event_no_connector() -> None:
    from outbox.v1 import destination_pb2 as d

    proto = d.DeliveryEvent()
    # No connector set → empty string

    result = map_delivery_event(proto)

    assert result.connector_id == ""


# --- Edge case tests ---


def test_proto_ts_zero_returns_none() -> None:
    """Zero timestamp (seconds=0, nanos=0) must return None."""
    from outbox_sdk._mappers import proto_ts

    ts = Timestamp()  # defaults to seconds=0, nanos=0
    assert proto_ts(ts) is None


def test_proto_ts_nanos_only() -> None:
    """Timestamp with only nanos set is non-zero, should return datetime."""
    from outbox_sdk._mappers import proto_ts

    ts = Timestamp()
    ts.nanos = 500_000_000  # 0.5 seconds
    result = proto_ts(ts)
    assert result is not None
    assert result.microsecond > 0


def test_map_connector_with_tags() -> None:
    proto = connector_pb2.Connector()
    proto.name = "connectors/abc"
    proto.tags.extend(["prod", "whatsapp", "critical"])
    proto.state = connector_pb2.ConnectorState.CONNECTOR_STATE_ACTIVE

    result = map_connector(proto)

    assert result.tags == ["prod", "whatsapp", "critical"]


def test_map_connector_no_tags() -> None:
    proto = connector_pb2.Connector()
    proto.name = "connectors/abc"
    proto.state = connector_pb2.ConnectorState.CONNECTOR_STATE_ACTIVE

    result = map_connector(proto)

    assert result.tags == []


def test_map_connector_channel_config_includes_all_fields() -> None:
    """channel_config mapper uses `if val is not None:` so all fields including empty strings are included."""
    proto = connector_pb2.Connector()
    proto.name = "connectors/abc"
    proto.state = connector_pb2.ConnectorState.CONNECTOR_STATE_ACTIVE
    proto.whatsapp_bot.app_id = ""  # empty string — now included (is not None)
    proto.whatsapp_bot.app_secret = "secret-123"

    result = map_connector(proto)

    assert result.channel_config_type == "whatsapp_bot"
    assert result.channel_config is not None
    assert result.channel_config["app_id"] == ""
    assert result.channel_config["app_secret"] == "secret-123"


def test_map_destination_multiple_event_types() -> None:
    proto = destination_pb2.Destination()
    proto.name = "destinations/d1"
    proto.display_name = "Multi-event"
    proto.state = destination_pb2.Destination.State.STATE_ACTIVE
    proto.event_types.extend(
        [
            destination_pb2.Destination.EventType.EVENT_TYPE_MESSAGE,
            destination_pb2.Destination.EventType.EVENT_TYPE_DELIVERY_UPDATE,
            destination_pb2.Destination.EventType.EVENT_TYPE_READ_RECEIPT,
            destination_pb2.Destination.EventType.EVENT_TYPE_TYPING_INDICATOR,
        ]
    )

    result = map_destination(proto)

    assert len(result.event_types) == 4
    assert DestinationEventType.MESSAGE in result.event_types
    assert DestinationEventType.DELIVERY_UPDATE in result.event_types
    assert DestinationEventType.READ_RECEIPT in result.event_types
    assert DestinationEventType.TYPING_INDICATOR in result.event_types


def test_map_destination_webhook_headers_dict() -> None:
    """Webhook headers map field should be converted to a Python dict."""
    proto = destination_pb2.Destination()
    proto.name = "destinations/d1"
    proto.display_name = "Webhook"
    proto.webhook.url = "https://example.com/hook"
    proto.webhook.headers["X-Custom"] = "my-value"
    proto.webhook.headers["Authorization"] = "Bearer tok"

    result = map_destination(proto)

    assert result.target_type == "webhook"
    assert result.target_config is not None
    assert result.target_config["headers"] == {"X-Custom": "my-value", "Authorization": "Bearer tok"}


def test_map_destination_kafka_target() -> None:
    """Kafka brokers is a comma-separated string, not a repeated field."""
    proto = destination_pb2.Destination()
    proto.name = "destinations/d1"
    proto.display_name = "Kafka"
    proto.kafka.brokers = "broker1:9092,broker2:9092"
    proto.kafka.topic = "events"

    result = map_destination(proto)

    assert result.target_type == "kafka"
    assert result.target_config is not None
    assert result.target_config["brokers"] == "broker1:9092,broker2:9092"
    assert result.target_config["topic"] == "events"


def test_map_destination_filter_expression() -> None:
    """Destination.filter_expression is mapped from proto filter field."""
    proto = destination_pb2.Destination()
    proto.name = "destinations/d1"
    proto.display_name = "Filtered"
    proto.filter = 'event.type == "message"'

    result = map_destination(proto)

    assert result.filter_expression == 'event.type == "message"'


def test_map_message_all_optional_fields() -> None:
    proto = message_pb2.Message()
    proto.name = "messages/msg-1"
    proto.recipient = "accounts/recip-1"
    proto.direction = message_pb2.Message.Direction.DIRECTION_OUTBOUND
    proto.account.name = "accounts/sender-1"
    proto.account.contact_id = "contact-1"
    proto.account.external_id = "ext-1"
    part = proto.parts.add()
    part.content_type = "text/plain"
    part.content = b"Hello"
    proto.metadata["key"] = "value"
    proto.reply_to = "messages/parent-msg"
    proto.group_id = "group-123"
    proto.edit_number = 2
    proto.create_time.CopyFrom(_ts(1700000000))
    proto.deliver_time.CopyFrom(_ts(1700000001))

    result = map_message(proto)

    assert result.edit_number == 2
    assert result.group_id == "group-123"
    assert result.reply_to_message_id == "parent-msg"
    assert len(result.parts) == 1
    assert result.metadata == {"key": "value"}
    assert result.account is not None
    assert result.deliver_time is not None
    assert result.create_time is not None


def test_map_message_minimal_fields() -> None:
    proto = message_pb2.Message()
    proto.name = "messages/msg-2"
    proto.recipient = "accounts/recip-1"

    result = map_message(proto)

    assert result.id == "msg-2"
    assert result.account is None
    assert result.parts == []
    assert result.metadata == {}
    assert result.reply_to_message_id is None
    assert result.group_id is None
    assert result.replaced_message_id is None
    assert result.delete_time is None


def test_map_delivery_event_all_metadata_fields() -> None:
    """delivery_id, destination_id, and enqueue_time are all mapped from the proto."""
    from datetime import UTC

    from outbox.v1 import destination_pb2 as d

    proto = d.DeliveryEvent()
    proto.connector = "connectors/conn-1"
    proto.destination = "destinations/dest-99"
    proto.delivery_id = "dlv-xyz"
    proto.enqueue_time.seconds = 1700000000
    proto.message.name = "messages/msg-1"
    proto.message.recipient = "accounts/recip-1"
    proto.message.direction = message_pb2.Message.Direction.DIRECTION_OUTBOUND

    result = map_delivery_event(proto)

    assert result.delivery_id == "dlv-xyz"
    assert result.destination_id == "dest-99"
    assert result.enqueue_time is not None
    assert result.enqueue_time.year == 2023
    assert result.enqueue_time.tzinfo == UTC


def test_map_delivery_event_no_destination() -> None:
    """destination_id defaults to empty string when not set."""
    from outbox.v1 import destination_pb2 as d

    proto = d.DeliveryEvent()
    proto.connector = "connectors/conn-1"
    # No destination set

    result = map_delivery_event(proto)

    assert result.destination_id == ""
    assert result.delivery_id == ""
    assert result.enqueue_time is None


def test_map_delivery_event_unknown_has_metadata_fields() -> None:
    """UnknownDeliveryEvent also carries delivery_id, destination_id, enqueue_time."""
    from outbox.v1 import destination_pb2 as d

    proto = d.DeliveryEvent()
    proto.connector = "connectors/conn-1"
    proto.destination = "destinations/dest-1"
    proto.delivery_id = "dlv-unknown"
    # No event set → unknown type

    result = map_delivery_event(proto)

    assert result.type == "unknown"
    assert result.delivery_id == "dlv-unknown"
    assert result.destination_id == "dest-1"


# --- Additional destination target type tests ---


def test_map_destination_temporal_target() -> None:
    from outbox.v1 import destination_pb2

    proto = destination_pb2.Destination()
    proto.name = "destinations/dest-1"
    proto.display_name = "My Temporal"
    proto.state = destination_pb2.Destination.State.STATE_ACTIVE
    proto.temporal.address = "temporal.example.com:7233"
    proto.temporal.namespace = "default"
    proto.temporal.task_queue = "my-queue"
    proto.temporal.workflow_type = "MyWorkflow"

    result = map_destination(proto)

    assert result.target_type == "temporal"
    assert result.target_config is not None
    assert result.target_config["address"] == "temporal.example.com:7233"
    assert result.target_config["namespace"] == "default"
    assert result.target_config["task_queue"] == "my-queue"
    assert result.target_config["workflow_type"] == "MyWorkflow"


def test_map_destination_sqs_target() -> None:
    from outbox.v1 import destination_pb2

    proto = destination_pb2.Destination()
    proto.name = "destinations/dest-2"
    proto.state = destination_pb2.Destination.State.STATE_ACTIVE
    proto.sqs.queue_url = "https://sqs.us-east-1.amazonaws.com/123/my-queue"
    proto.sqs.region = "us-east-1"
    proto.sqs.access_key_id = "AKIAIOSFODNN7EXAMPLE"
    proto.sqs.secret_access_key = "wJalrXUtnFEMI"

    result = map_destination(proto)

    assert result.target_type == "sqs"
    assert result.target_config is not None
    assert result.target_config["queue_url"] == "https://sqs.us-east-1.amazonaws.com/123/my-queue"
    assert result.target_config["region"] == "us-east-1"
    assert result.target_config["access_key_id"] == "AKIAIOSFODNN7EXAMPLE"


def test_map_destination_smtp_target() -> None:
    from outbox.v1 import destination_pb2

    proto = destination_pb2.Destination()
    proto.name = "destinations/dest-3"
    proto.state = destination_pb2.Destination.State.STATE_ACTIVE
    proto.smtp.host = "smtp.example.com"
    proto.smtp.port = 587
    proto.smtp.username = "user@example.com"
    proto.smtp.password = "secret"
    proto.smtp.from_address = "noreply@example.com"
    proto.smtp.to_address = "dest@example.com"
    proto.smtp.require_tls = True

    result = map_destination(proto)

    assert result.target_type == "smtp"
    assert result.target_config is not None
    assert result.target_config["host"] == "smtp.example.com"
    assert result.target_config["port"] == 587
    assert result.target_config["require_tls"] is True


def test_map_destination_google_pub_sub_target() -> None:
    from outbox.v1 import destination_pb2

    proto = destination_pb2.Destination()
    proto.name = "destinations/dest-4"
    proto.state = destination_pb2.Destination.State.STATE_ACTIVE
    proto.google_pub_sub.project_id = "my-project"
    proto.google_pub_sub.topic_id = "my-topic"
    proto.google_pub_sub.credentials_json = '{"type": "service_account"}'

    result = map_destination(proto)

    assert result.target_type == "google_pub_sub"
    assert result.target_config is not None
    assert result.target_config["project_id"] == "my-project"
    assert result.target_config["topic_id"] == "my-topic"


def test_map_connector_empty_string_config_preserved() -> None:
    """An empty string field must appear in channel_config (val is not None)."""
    from outbox.v1 import connector_pb2

    proto = connector_pb2.Connector()
    proto.name = "connectors/conn-1"
    proto.state = connector_pb2.ConnectorState.CONNECTOR_STATE_ACTIVE
    # slack_bot.bot_token is an empty string — it must still be included
    proto.slack_bot.bot_token = ""  # empty string, same as proto default
    proto.slack_bot.signing_secret = "sign-abc"

    result = map_connector(proto)

    assert result.channel_config_type == "slack_bot"
    assert result.channel_config is not None
    assert result.channel_config["bot_token"] == ""
    assert result.channel_config["signing_secret"] == "sign-abc"


def test_map_destination_restate_target() -> None:
    from outbox.v1 import destination_pb2

    proto = destination_pb2.Destination()
    proto.name = "destinations/dest-1"
    proto.state = destination_pb2.Destination.State.STATE_ACTIVE
    proto.restate.url = "https://restate.example.com"
    proto.restate.headers["Authorization"] = "Bearer token"

    result = map_destination(proto)

    assert result.target_type == "restate"
    assert result.target_config is not None
    assert result.target_config["url"] == "https://restate.example.com"
    assert result.target_config["headers"] == {"Authorization": "Bearer token"}


def test_map_destination_inngest_target() -> None:
    from outbox.v1 import destination_pb2

    proto = destination_pb2.Destination()
    proto.name = "destinations/dest-2"
    proto.state = destination_pb2.Destination.State.STATE_ACTIVE
    proto.inngest.url = "https://api.inngest.com"
    proto.inngest.event_key = "my-event-key"
    proto.inngest.event_name = "outbox.message.sent"

    result = map_destination(proto)

    assert result.target_type == "inngest"
    assert result.target_config is not None
    assert result.target_config["url"] == "https://api.inngest.com"
    assert result.target_config["event_key"] == "my-event-key"
    assert result.target_config["event_name"] == "outbox.message.sent"


def test_map_destination_cloudflare_worker_target() -> None:
    from outbox.v1 import destination_pb2

    proto = destination_pb2.Destination()
    proto.name = "destinations/dest-3"
    proto.state = destination_pb2.Destination.State.STATE_ACTIVE
    proto.cloudflare_worker.url = "https://worker.example.workers.dev"
    proto.cloudflare_worker.cf_access_client_id = "client-id-123"
    proto.cloudflare_worker.cf_access_client_secret = "secret-xyz"
    proto.cloudflare_worker.headers["X-Custom"] = "value"

    result = map_destination(proto)

    assert result.target_type == "cloudflare_worker"
    assert result.target_config is not None
    assert result.target_config["url"] == "https://worker.example.workers.dev"
    assert result.target_config["cf_access_client_id"] == "client-id-123"
    assert result.target_config["cf_access_client_secret"] == "secret-xyz"
    assert result.target_config["headers"] == {"X-Custom": "value"}


def test_map_destination_golem_target() -> None:
    from outbox.v1 import destination_pb2

    proto = destination_pb2.Destination()
    proto.name = "destinations/dest-4"
    proto.state = destination_pb2.Destination.State.STATE_ACTIVE
    proto.golem.url = "http://localhost:9001"
    proto.golem.component_id = "comp-abc"
    proto.golem.worker_name = "worker-1"
    proto.golem.function_name = "handle_event"
    proto.golem.api_token = "golem-token"

    result = map_destination(proto)

    assert result.target_type == "golem"
    assert result.target_config is not None
    assert result.target_config["url"] == "http://localhost:9001"
    assert result.target_config["component_id"] == "comp-abc"
    assert result.target_config["worker_name"] == "worker-1"
    assert result.target_config["function_name"] == "handle_event"
    assert result.target_config["api_token"] == "golem-token"


def test_map_destination_hatchet_target() -> None:
    from outbox.v1 import destination_pb2

    proto = destination_pb2.Destination()
    proto.name = "destinations/dest-5"
    proto.state = destination_pb2.Destination.State.STATE_ACTIVE
    proto.hatchet.address = "hatchet.example.com:8080"
    proto.hatchet.workflow_name = "process_message"
    proto.hatchet.api_token = "hatchet-api-key"

    result = map_destination(proto)

    assert result.target_type == "hatchet"
    assert result.target_config is not None
    assert result.target_config["address"] == "hatchet.example.com:8080"
    assert result.target_config["workflow_name"] == "process_message"
    assert result.target_config["api_token"] == "hatchet-api-key"


def test_map_destination_sns_target() -> None:
    from outbox.v1 import destination_pb2

    proto = destination_pb2.Destination()
    proto.name = "destinations/dest-6"
    proto.state = destination_pb2.Destination.State.STATE_ACTIVE
    proto.sns.topic_arn = "arn:aws:sns:us-east-1:123456789012:my-topic"
    proto.sns.region = "us-east-1"
    proto.sns.access_key_id = "AKIAIOSFODNN7EXAMPLE"
    proto.sns.secret_access_key = "wJalrXUtnFEMI"

    result = map_destination(proto)

    assert result.target_type == "sns"
    assert result.target_config is not None
    assert result.target_config["topic_arn"] == "arn:aws:sns:us-east-1:123456789012:my-topic"
    assert result.target_config["region"] == "us-east-1"
    assert result.target_config["access_key_id"] == "AKIAIOSFODNN7EXAMPLE"


def test_map_destination_event_bridge_target() -> None:
    from outbox.v1 import destination_pb2

    proto = destination_pb2.Destination()
    proto.name = "destinations/dest-7"
    proto.state = destination_pb2.Destination.State.STATE_ACTIVE
    proto.event_bridge.event_bus = "custom-bus"
    proto.event_bridge.detail_type = "Message Delivered"
    proto.event_bridge.source = "outbox.service"
    proto.event_bridge.region = "us-west-2"
    proto.event_bridge.access_key_id = "AKIAEXAMPLE"
    proto.event_bridge.secret_access_key = "secretkey"

    result = map_destination(proto)

    assert result.target_type == "event_bridge"
    assert result.target_config is not None
    assert result.target_config["event_bus"] == "custom-bus"
    assert result.target_config["detail_type"] == "Message Delivered"
    assert result.target_config["source"] == "outbox.service"
    assert result.target_config["region"] == "us-west-2"


def test_map_destination_nats_target() -> None:
    from outbox.v1 import destination_pb2

    proto = destination_pb2.Destination()
    proto.name = "destinations/dest-8"
    proto.state = destination_pb2.Destination.State.STATE_ACTIVE
    proto.nats.url = "nats://localhost:4222"
    proto.nats.subject = "outbox.events"
    proto.nats.username = "user123"
    proto.nats.password = "pass456"
    proto.nats.token = "nats-token"

    result = map_destination(proto)

    assert result.target_type == "nats"
    assert result.target_config is not None
    assert result.target_config["url"] == "nats://localhost:4222"
    assert result.target_config["subject"] == "outbox.events"
    assert result.target_config["username"] == "user123"
    assert result.target_config["password"] == "pass456"
    assert result.target_config["token"] == "nats-token"


# --- Template mapper tests ---


def test_map_template_basic() -> None:
    proto = template_pb2.Template()
    proto.name = "connectors/conn-1/templates/tmpl-abc"
    proto.template_name = "order_confirmation"
    proto.language = "en"
    proto.category = template_pb2.Template.Category.CATEGORY_UTILITY
    proto.components_json = '[{"type":"BODY","text":"Hello"}]'
    proto.status = template_pb2.TemplateStatus.TEMPLATE_STATUS_APPROVED
    proto.create_time.CopyFrom(_ts(1700000000))
    proto.update_time.CopyFrom(_ts(1700000001))

    result = map_template(proto)

    assert result.id == "tmpl-abc"
    assert result.connector_id == "conn-1"
    assert result.template_name == "order_confirmation"
    assert result.language == "en"
    assert result.category == TemplateCategory.UTILITY
    assert result.components_json == '[{"type":"BODY","text":"Hello"}]'
    assert result.status == TemplateStatus.APPROVED
    assert result.create_time is not None
    assert result.update_time is not None


def test_map_template_rejection() -> None:
    proto = template_pb2.Template()
    proto.name = "connectors/conn-1/templates/tmpl-rej"
    proto.template_name = "promo"
    proto.language = "es"
    proto.category = template_pb2.Template.Category.CATEGORY_MARKETING
    proto.status = template_pb2.TemplateStatus.TEMPLATE_STATUS_REJECTED
    proto.rejection_reason = "content policy violation"
    proto.external_id = "ext-12345"

    result = map_template(proto)

    assert result.id == "tmpl-rej"
    assert result.connector_id == "conn-1"
    assert result.category == TemplateCategory.MARKETING
    assert result.status == TemplateStatus.REJECTED
    assert result.rejection_reason == "content policy violation"
    assert result.external_id == "ext-12345"
    assert result.create_time is None
    assert result.update_time is None


def test_map_template_status_paused() -> None:
    tmpl = template_pb2.Template()
    tmpl.name = "connectors/c1/templates/t1"
    tmpl.status = template_pb2.TemplateStatus.TEMPLATE_STATUS_PAUSED
    result = map_template(tmpl)
    assert result.status == TemplateStatus.PAUSED


def test_map_template_status_disabled() -> None:
    tmpl = template_pb2.Template()
    tmpl.name = "connectors/c1/templates/t1"
    tmpl.status = template_pb2.TemplateStatus.TEMPLATE_STATUS_DISABLED
    result = map_template(tmpl)
    assert result.status == TemplateStatus.DISABLED


def test_map_template_malformed_name() -> None:
    tmpl = template_pb2.Template()
    tmpl.name = "bad-name"
    with pytest.raises(ValueError, match="Invalid template resource name"):
        map_template(tmpl)


def test_map_template_wrong_prefix() -> None:
    tmpl = template_pb2.Template()
    tmpl.name = "foo/conn-1/bar/tmpl-1"
    with pytest.raises(ValueError, match="Invalid template resource name"):
        map_template(tmpl)
