from __future__ import annotations

from datetime import UTC, datetime
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from google.protobuf.timestamp_pb2 import Timestamp
    from outbox.v1.account_pb2 import Account as ProtoAccount
    from outbox.v1.connector_pb2 import Connector as ProtoConnector
    from outbox.v1.destination_pb2 import DeliveryEvent as ProtoDeliveryEvent
    from outbox.v1.destination_pb2 import Destination as ProtoDestination
    from outbox.v1.message_pb2 import Message as ProtoMessage
    from outbox.v1.message_pb2 import MessageDelivery as ProtoMessageDelivery
    from outbox.v1.message_pb2 import MessagePart as ProtoMessagePart
    from outbox.v1.message_pb2 import ReadReceiptEvent as ProtoReadReceiptEvent
    from outbox.v1.message_pb2 import TypingIndicatorEvent as ProtoTypingIndicatorEvent
    from outbox.v1.template_pb2 import Template as ProtoTemplate

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
from outbox_sdk._resource_names import parse_id
from outbox_sdk._types import (
    Account,
    Connector,
    DeliveryEvent,
    DeliveryUpdateEvent,
    Destination,
    Message,
    MessageDelivery,
    MessageEvent,
    MessagePart,
    ReadReceiptDeliveryEvent,
    ReadReceiptEvent,
    Template,
    TypingIndicatorDeliveryEvent,
    TypingIndicatorEvent,
    UnknownDeliveryEvent,
)


def proto_ts(ts: Timestamp) -> datetime | None:
    """Convert a protobuf Timestamp to a UTC datetime."""
    if ts.seconds == 0 and ts.nanos == 0:
        return None
    return datetime.fromtimestamp(ts.seconds + ts.nanos / 1_000_000_000, tz=UTC)


def map_connector(p: ProtoConnector) -> Connector:
    which = p.WhichOneof("channel_config")
    config_dict: dict[str, object] | None = None
    if which:
        config_obj = getattr(p, which)
        config_dict = {}
        # Note: proto3 scalar zero-values ("", 0, False) are never None, so they are
        # always included in the config dict. This is intentional — callers receive
        # the full config as the server set it.
        for field in config_obj.DESCRIPTOR.fields:
            val = getattr(config_obj, field.name)
            if field.is_repeated:
                config_dict[field.name] = list(val)
            elif val is not None:
                if hasattr(val, "items"):
                    val = dict(val)
                config_dict[field.name] = val
    provisioned_resources = [parse_id(r) for r in p.provisioned_resources]
    return Connector(
        id=parse_id(p.name),
        kind=ConnectorKind(p.kind),
        state=ConnectorState(p.state),
        readiness=ConnectorReadiness(p.readiness),
        provisioned_resources=provisioned_resources,
        webhook_url=p.webhook_url,
        display_name=p.display_name,
        tags=list(p.tags),
        channel_config_type=which or None,
        channel_config=config_dict,
        error_message=p.error_message or None,
        create_time=proto_ts(p.create_time),
        update_time=proto_ts(p.update_time),
    )


def map_template(p: ProtoTemplate) -> Template:
    name = p.name
    parts = name.split("/")
    if len(parts) < 4 or not parts[1] or not parts[3]:
        raise ValueError(f"Invalid template resource name: {name!r}")
    if parts[0] != "connectors" or parts[2] != "templates":
        raise ValueError(f"Invalid template resource name: {name!r}")
    connector_id = parts[1]
    template_id = parts[3]
    return Template(
        id=template_id,
        connector_id=connector_id,
        template_name=p.template_name,
        language=p.language,
        category=TemplateCategory(p.category),
        components_json=p.components_json,
        status=TemplateStatus(p.status),
        rejection_reason=p.rejection_reason,
        external_id=p.external_id,
        create_time=proto_ts(p.create_time),
        update_time=proto_ts(p.update_time),
    )


def map_account(p: ProtoAccount) -> Account:
    return Account(
        id=parse_id(p.name),
        contact_id=p.contact_id,
        external_id=p.external_id,
        metadata=dict(p.metadata),
        source=AccountSource(p.source),
        create_time=proto_ts(p.create_time),
        update_time=proto_ts(p.update_time),
    )


def map_message_part(p: ProtoMessagePart) -> MessagePart:
    content: bytes | None = p.content or None
    url: str | None = p.url or None
    return MessagePart(
        content_type=p.content_type,
        disposition=MessagePartDisposition(p.disposition),
        content=content,
        url=url,
        filename=p.filename or None,
    )


def map_message(p: ProtoMessage) -> Message:
    return Message(
        id=parse_id(p.name),
        account=map_account(p.account) if p.HasField("account") else None,
        recipient_id=parse_id(p.recipient),
        parts=[map_message_part(part) for part in p.parts],
        metadata=dict(p.metadata),
        direction=MessageDirection(p.direction),
        deletion_scope=MessageDeletionScope(p.scope),
        edit_number=p.edit_number,
        create_time=proto_ts(p.create_time),
        deliver_time=proto_ts(p.deliver_time),
        delete_time=proto_ts(p.delete_time) if p.HasField("delete_time") else None,
        reply_to_message_id=parse_id(p.reply_to) if p.reply_to else None,
        group_id=p.group_id or None,
        replaced_message_id=parse_id(p.replaced) if p.HasField("replaced") else None,
    )


def map_message_delivery(p: ProtoMessageDelivery) -> MessageDelivery:
    return MessageDelivery(
        message_id=parse_id(p.message),
        account=map_account(p.account) if p.HasField("account") else None,
        status=MessageDeliveryStatus(p.status),
        error_code=p.error_code,
        error_message=p.error_message,
        status_change_time=proto_ts(p.status_change_time),
    )


def map_read_receipt(p: ProtoReadReceiptEvent) -> ReadReceiptEvent:
    return ReadReceiptEvent(
        account=map_account(p.account) if p.HasField("account") else None,
        message_ids=[parse_id(n) for n in p.messages],
        timestamp=proto_ts(p.timestamp),
    )


def map_typing_indicator(p: ProtoTypingIndicatorEvent) -> TypingIndicatorEvent:
    return TypingIndicatorEvent(
        account=map_account(p.account) if p.HasField("account") else None,
        typing=p.typing,
        content_type=p.content_type or None,
        timestamp=proto_ts(p.timestamp),
    )


_TARGET_FIELDS = {
    "webhook": ("url", "signing_secret", "headers"),
    "temporal": (
        "address",
        "namespace",
        "task_queue",
        "workflow_type",
        "api_key",
        "tls_cert_pem",
        "tls_key_pem",
    ),
    "restate": ("url", "headers"),
    "inngest": ("url", "event_key", "event_name"),
    "cloudflare_worker": ("url", "cf_access_client_id", "cf_access_client_secret", "headers"),
    "golem": ("url", "component_id", "worker_name", "function_name", "api_token"),
    "hatchet": ("address", "workflow_name", "api_token"),
    "sqs": ("queue_url", "region", "access_key_id", "secret_access_key", "message_group_id"),
    "sns": ("topic_arn", "region", "access_key_id", "secret_access_key"),
    "event_bridge": ("event_bus", "detail_type", "source", "region", "access_key_id", "secret_access_key"),
    "kafka": ("brokers", "topic", "sasl_username", "sasl_password", "sasl_mechanism", "tls_enabled"),
    "google_pub_sub": ("project_id", "topic_id", "credentials_json"),
    "nats": ("url", "subject", "credentials", "username", "password", "token"),
    "smtp": ("host", "port", "username", "password", "from_address", "to_address", "subject_template", "require_tls"),
    "rabbit_mq": ("url", "exchange", "routing_key"),
    "azure_service_bus": ("connection_string", "queue_or_topic"),
    "redis": ("url", "stream_key"),
}


def map_delivery_event(p: ProtoDeliveryEvent) -> DeliveryEvent:
    # connector is always set by the server; empty string indicates a malformed event
    connector_id = parse_id(p.connector) if p.connector else ""
    destination_id = parse_id(p.destination) if p.destination else ""
    delivery_id = p.delivery_id
    enqueue_time = proto_ts(p.enqueue_time)
    which = p.WhichOneof("event")
    if which == "message":
        return MessageEvent(
            connector_id=connector_id,
            delivery_id=delivery_id,
            destination_id=destination_id,
            enqueue_time=enqueue_time,
            message=map_message(p.message),
        )
    if which == "delivery_update":
        return DeliveryUpdateEvent(
            connector_id=connector_id,
            delivery_id=delivery_id,
            destination_id=destination_id,
            enqueue_time=enqueue_time,
            delivery_update=map_message_delivery(p.delivery_update),
        )
    if which == "read_receipt":
        return ReadReceiptDeliveryEvent(
            connector_id=connector_id,
            delivery_id=delivery_id,
            destination_id=destination_id,
            enqueue_time=enqueue_time,
            read_receipt=map_read_receipt(p.read_receipt),
        )
    if which == "typing_indicator":
        return TypingIndicatorDeliveryEvent(
            connector_id=connector_id,
            delivery_id=delivery_id,
            destination_id=destination_id,
            enqueue_time=enqueue_time,
            typing_indicator=map_typing_indicator(p.typing_indicator),
        )
    return UnknownDeliveryEvent(
        connector_id=connector_id,
        delivery_id=delivery_id,
        destination_id=destination_id,
        enqueue_time=enqueue_time,
    )


def map_destination(p: ProtoDestination) -> Destination:
    target_type = p.WhichOneof("target")
    target_config: dict[str, object] | None = None

    if target_type:
        target_obj = getattr(p, target_type, None)
        if target_obj is not None:
            fields = _TARGET_FIELDS.get(target_type, ())
            target_config = {}
            for f in fields:
                val = getattr(target_obj, f, None)
                if val is not None:
                    if hasattr(val, "items"):
                        val = dict(val)
                    elif hasattr(val, "__iter__") and not isinstance(val, (str, bytes)):
                        val = list(val)
                    target_config[f] = val

    return Destination(
        id=parse_id(p.name),
        display_name=p.display_name,
        state=DestinationState(p.state),
        event_types=[DestinationEventType(et) for et in p.event_types],
        filter_expression=p.filter,
        payload_format=DestinationPayloadFormat(p.payload_format),
        target_type=target_type,
        target_config=target_config,
        create_time=proto_ts(p.create_time),
        update_time=proto_ts(p.update_time),
        last_test_time=proto_ts(p.last_test_time),
        last_test_success=p.last_test_success,
    )
