import datetime

from buf.validate import validate_pb2 as _validate_pb2
from google.api import client_pb2 as _client_pb2
from google.api import field_behavior_pb2 as _field_behavior_pb2
from google.api import field_info_pb2 as _field_info_pb2
from google.api import resource_pb2 as _resource_pb2
from google.protobuf import field_mask_pb2 as _field_mask_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from outbox.v1 import message_pb2 as _message_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class WebhookTarget(_message.Message):
    __slots__ = ("url", "signing_secret", "headers")
    class HeadersEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    URL_FIELD_NUMBER: _ClassVar[int]
    SIGNING_SECRET_FIELD_NUMBER: _ClassVar[int]
    HEADERS_FIELD_NUMBER: _ClassVar[int]
    url: str
    signing_secret: str
    headers: _containers.ScalarMap[str, str]
    def __init__(self, url: _Optional[str] = ..., signing_secret: _Optional[str] = ..., headers: _Optional[_Mapping[str, str]] = ...) -> None: ...

class TemporalTarget(_message.Message):
    __slots__ = ("address", "namespace", "task_queue", "workflow_type", "api_key", "tls_cert_pem", "tls_key_pem")
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    TASK_QUEUE_FIELD_NUMBER: _ClassVar[int]
    WORKFLOW_TYPE_FIELD_NUMBER: _ClassVar[int]
    API_KEY_FIELD_NUMBER: _ClassVar[int]
    TLS_CERT_PEM_FIELD_NUMBER: _ClassVar[int]
    TLS_KEY_PEM_FIELD_NUMBER: _ClassVar[int]
    address: str
    namespace: str
    task_queue: str
    workflow_type: str
    api_key: str
    tls_cert_pem: str
    tls_key_pem: str
    def __init__(self, address: _Optional[str] = ..., namespace: _Optional[str] = ..., task_queue: _Optional[str] = ..., workflow_type: _Optional[str] = ..., api_key: _Optional[str] = ..., tls_cert_pem: _Optional[str] = ..., tls_key_pem: _Optional[str] = ...) -> None: ...

class GolemTarget(_message.Message):
    __slots__ = ("url", "component_id", "worker_name", "function_name", "api_token")
    URL_FIELD_NUMBER: _ClassVar[int]
    COMPONENT_ID_FIELD_NUMBER: _ClassVar[int]
    WORKER_NAME_FIELD_NUMBER: _ClassVar[int]
    FUNCTION_NAME_FIELD_NUMBER: _ClassVar[int]
    API_TOKEN_FIELD_NUMBER: _ClassVar[int]
    url: str
    component_id: str
    worker_name: str
    function_name: str
    api_token: str
    def __init__(self, url: _Optional[str] = ..., component_id: _Optional[str] = ..., worker_name: _Optional[str] = ..., function_name: _Optional[str] = ..., api_token: _Optional[str] = ...) -> None: ...

class RestateTarget(_message.Message):
    __slots__ = ("url", "headers")
    class HeadersEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    URL_FIELD_NUMBER: _ClassVar[int]
    HEADERS_FIELD_NUMBER: _ClassVar[int]
    url: str
    headers: _containers.ScalarMap[str, str]
    def __init__(self, url: _Optional[str] = ..., headers: _Optional[_Mapping[str, str]] = ...) -> None: ...

class InngestTarget(_message.Message):
    __slots__ = ("url", "event_key", "event_name")
    URL_FIELD_NUMBER: _ClassVar[int]
    EVENT_KEY_FIELD_NUMBER: _ClassVar[int]
    EVENT_NAME_FIELD_NUMBER: _ClassVar[int]
    url: str
    event_key: str
    event_name: str
    def __init__(self, url: _Optional[str] = ..., event_key: _Optional[str] = ..., event_name: _Optional[str] = ...) -> None: ...

class HatchetTarget(_message.Message):
    __slots__ = ("address", "workflow_name", "api_token")
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    WORKFLOW_NAME_FIELD_NUMBER: _ClassVar[int]
    API_TOKEN_FIELD_NUMBER: _ClassVar[int]
    address: str
    workflow_name: str
    api_token: str
    def __init__(self, address: _Optional[str] = ..., workflow_name: _Optional[str] = ..., api_token: _Optional[str] = ...) -> None: ...

class SqsTarget(_message.Message):
    __slots__ = ("queue_url", "region", "access_key_id", "secret_access_key", "message_group_id")
    QUEUE_URL_FIELD_NUMBER: _ClassVar[int]
    REGION_FIELD_NUMBER: _ClassVar[int]
    ACCESS_KEY_ID_FIELD_NUMBER: _ClassVar[int]
    SECRET_ACCESS_KEY_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_GROUP_ID_FIELD_NUMBER: _ClassVar[int]
    queue_url: str
    region: str
    access_key_id: str
    secret_access_key: str
    message_group_id: str
    def __init__(self, queue_url: _Optional[str] = ..., region: _Optional[str] = ..., access_key_id: _Optional[str] = ..., secret_access_key: _Optional[str] = ..., message_group_id: _Optional[str] = ...) -> None: ...

class SnsTarget(_message.Message):
    __slots__ = ("topic_arn", "region", "access_key_id", "secret_access_key")
    TOPIC_ARN_FIELD_NUMBER: _ClassVar[int]
    REGION_FIELD_NUMBER: _ClassVar[int]
    ACCESS_KEY_ID_FIELD_NUMBER: _ClassVar[int]
    SECRET_ACCESS_KEY_FIELD_NUMBER: _ClassVar[int]
    topic_arn: str
    region: str
    access_key_id: str
    secret_access_key: str
    def __init__(self, topic_arn: _Optional[str] = ..., region: _Optional[str] = ..., access_key_id: _Optional[str] = ..., secret_access_key: _Optional[str] = ...) -> None: ...

class EventBridgeTarget(_message.Message):
    __slots__ = ("event_bus", "detail_type", "source", "region", "access_key_id", "secret_access_key")
    EVENT_BUS_FIELD_NUMBER: _ClassVar[int]
    DETAIL_TYPE_FIELD_NUMBER: _ClassVar[int]
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    REGION_FIELD_NUMBER: _ClassVar[int]
    ACCESS_KEY_ID_FIELD_NUMBER: _ClassVar[int]
    SECRET_ACCESS_KEY_FIELD_NUMBER: _ClassVar[int]
    event_bus: str
    detail_type: str
    source: str
    region: str
    access_key_id: str
    secret_access_key: str
    def __init__(self, event_bus: _Optional[str] = ..., detail_type: _Optional[str] = ..., source: _Optional[str] = ..., region: _Optional[str] = ..., access_key_id: _Optional[str] = ..., secret_access_key: _Optional[str] = ...) -> None: ...

class KafkaTarget(_message.Message):
    __slots__ = ("brokers", "topic", "sasl_username", "sasl_password", "sasl_mechanism", "tls_enabled")
    BROKERS_FIELD_NUMBER: _ClassVar[int]
    TOPIC_FIELD_NUMBER: _ClassVar[int]
    SASL_USERNAME_FIELD_NUMBER: _ClassVar[int]
    SASL_PASSWORD_FIELD_NUMBER: _ClassVar[int]
    SASL_MECHANISM_FIELD_NUMBER: _ClassVar[int]
    TLS_ENABLED_FIELD_NUMBER: _ClassVar[int]
    brokers: str
    topic: str
    sasl_username: str
    sasl_password: str
    sasl_mechanism: str
    tls_enabled: bool
    def __init__(self, brokers: _Optional[str] = ..., topic: _Optional[str] = ..., sasl_username: _Optional[str] = ..., sasl_password: _Optional[str] = ..., sasl_mechanism: _Optional[str] = ..., tls_enabled: _Optional[bool] = ...) -> None: ...

class GooglePubSubTarget(_message.Message):
    __slots__ = ("project_id", "topic_id", "credentials_json")
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    TOPIC_ID_FIELD_NUMBER: _ClassVar[int]
    CREDENTIALS_JSON_FIELD_NUMBER: _ClassVar[int]
    project_id: str
    topic_id: str
    credentials_json: str
    def __init__(self, project_id: _Optional[str] = ..., topic_id: _Optional[str] = ..., credentials_json: _Optional[str] = ...) -> None: ...

class NatsTarget(_message.Message):
    __slots__ = ("url", "subject", "credentials", "username", "password", "token")
    URL_FIELD_NUMBER: _ClassVar[int]
    SUBJECT_FIELD_NUMBER: _ClassVar[int]
    CREDENTIALS_FIELD_NUMBER: _ClassVar[int]
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    url: str
    subject: str
    credentials: str
    username: str
    password: str
    token: str
    def __init__(self, url: _Optional[str] = ..., subject: _Optional[str] = ..., credentials: _Optional[str] = ..., username: _Optional[str] = ..., password: _Optional[str] = ..., token: _Optional[str] = ...) -> None: ...

class RabbitMqTarget(_message.Message):
    __slots__ = ("url", "exchange", "routing_key")
    URL_FIELD_NUMBER: _ClassVar[int]
    EXCHANGE_FIELD_NUMBER: _ClassVar[int]
    ROUTING_KEY_FIELD_NUMBER: _ClassVar[int]
    url: str
    exchange: str
    routing_key: str
    def __init__(self, url: _Optional[str] = ..., exchange: _Optional[str] = ..., routing_key: _Optional[str] = ...) -> None: ...

class AzureServiceBusTarget(_message.Message):
    __slots__ = ("connection_string", "queue_or_topic")
    CONNECTION_STRING_FIELD_NUMBER: _ClassVar[int]
    QUEUE_OR_TOPIC_FIELD_NUMBER: _ClassVar[int]
    connection_string: str
    queue_or_topic: str
    def __init__(self, connection_string: _Optional[str] = ..., queue_or_topic: _Optional[str] = ...) -> None: ...

class RedisTarget(_message.Message):
    __slots__ = ("url", "stream_key")
    URL_FIELD_NUMBER: _ClassVar[int]
    STREAM_KEY_FIELD_NUMBER: _ClassVar[int]
    url: str
    stream_key: str
    def __init__(self, url: _Optional[str] = ..., stream_key: _Optional[str] = ...) -> None: ...

class SmtpTarget(_message.Message):
    __slots__ = ("host", "port", "username", "password", "from_address", "to_address", "subject_template", "require_tls")
    HOST_FIELD_NUMBER: _ClassVar[int]
    PORT_FIELD_NUMBER: _ClassVar[int]
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    FROM_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    TO_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    SUBJECT_TEMPLATE_FIELD_NUMBER: _ClassVar[int]
    REQUIRE_TLS_FIELD_NUMBER: _ClassVar[int]
    host: str
    port: int
    username: str
    password: str
    from_address: str
    to_address: str
    subject_template: str
    require_tls: bool
    def __init__(self, host: _Optional[str] = ..., port: _Optional[int] = ..., username: _Optional[str] = ..., password: _Optional[str] = ..., from_address: _Optional[str] = ..., to_address: _Optional[str] = ..., subject_template: _Optional[str] = ..., require_tls: _Optional[bool] = ...) -> None: ...

class LambdaTarget(_message.Message):
    __slots__ = ("url", "headers")
    class HeadersEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    URL_FIELD_NUMBER: _ClassVar[int]
    HEADERS_FIELD_NUMBER: _ClassVar[int]
    url: str
    headers: _containers.ScalarMap[str, str]
    def __init__(self, url: _Optional[str] = ..., headers: _Optional[_Mapping[str, str]] = ...) -> None: ...

class CloudflareWorkerTarget(_message.Message):
    __slots__ = ("url", "cf_access_client_id", "cf_access_client_secret", "headers")
    class HeadersEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    URL_FIELD_NUMBER: _ClassVar[int]
    CF_ACCESS_CLIENT_ID_FIELD_NUMBER: _ClassVar[int]
    CF_ACCESS_CLIENT_SECRET_FIELD_NUMBER: _ClassVar[int]
    HEADERS_FIELD_NUMBER: _ClassVar[int]
    url: str
    cf_access_client_id: str
    cf_access_client_secret: str
    headers: _containers.ScalarMap[str, str]
    def __init__(self, url: _Optional[str] = ..., cf_access_client_id: _Optional[str] = ..., cf_access_client_secret: _Optional[str] = ..., headers: _Optional[_Mapping[str, str]] = ...) -> None: ...

class LocalTarget(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class Destination(_message.Message):
    __slots__ = ("name", "display_name", "state", "event_types", "filter", "payload_format", "create_time", "update_time", "last_test_time", "last_test_success", "webhook", "restate", "inngest", "cloudflare_worker", "temporal", "golem", "hatchet", "sqs", "sns", "event_bridge", "kafka", "google_pub_sub", "nats", "smtp", "rabbit_mq", "azure_service_bus", "redis", "local")
    class State(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        STATE_UNSPECIFIED: _ClassVar[Destination.State]
        STATE_ACTIVE: _ClassVar[Destination.State]
        STATE_PAUSED: _ClassVar[Destination.State]
        STATE_DEGRADED: _ClassVar[Destination.State]
    STATE_UNSPECIFIED: Destination.State
    STATE_ACTIVE: Destination.State
    STATE_PAUSED: Destination.State
    STATE_DEGRADED: Destination.State
    class EventType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        EVENT_TYPE_UNSPECIFIED: _ClassVar[Destination.EventType]
        EVENT_TYPE_MESSAGE: _ClassVar[Destination.EventType]
        EVENT_TYPE_DELIVERY_UPDATE: _ClassVar[Destination.EventType]
        EVENT_TYPE_READ_RECEIPT: _ClassVar[Destination.EventType]
        EVENT_TYPE_TYPING_INDICATOR: _ClassVar[Destination.EventType]
    EVENT_TYPE_UNSPECIFIED: Destination.EventType
    EVENT_TYPE_MESSAGE: Destination.EventType
    EVENT_TYPE_DELIVERY_UPDATE: Destination.EventType
    EVENT_TYPE_READ_RECEIPT: Destination.EventType
    EVENT_TYPE_TYPING_INDICATOR: Destination.EventType
    class PayloadFormat(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        PAYLOAD_FORMAT_UNSPECIFIED: _ClassVar[Destination.PayloadFormat]
        PAYLOAD_FORMAT_JSON: _ClassVar[Destination.PayloadFormat]
        PAYLOAD_FORMAT_PROTO_BINARY: _ClassVar[Destination.PayloadFormat]
    PAYLOAD_FORMAT_UNSPECIFIED: Destination.PayloadFormat
    PAYLOAD_FORMAT_JSON: Destination.PayloadFormat
    PAYLOAD_FORMAT_PROTO_BINARY: Destination.PayloadFormat
    NAME_FIELD_NUMBER: _ClassVar[int]
    DISPLAY_NAME_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    EVENT_TYPES_FIELD_NUMBER: _ClassVar[int]
    FILTER_FIELD_NUMBER: _ClassVar[int]
    PAYLOAD_FORMAT_FIELD_NUMBER: _ClassVar[int]
    CREATE_TIME_FIELD_NUMBER: _ClassVar[int]
    UPDATE_TIME_FIELD_NUMBER: _ClassVar[int]
    LAST_TEST_TIME_FIELD_NUMBER: _ClassVar[int]
    LAST_TEST_SUCCESS_FIELD_NUMBER: _ClassVar[int]
    WEBHOOK_FIELD_NUMBER: _ClassVar[int]
    RESTATE_FIELD_NUMBER: _ClassVar[int]
    INNGEST_FIELD_NUMBER: _ClassVar[int]
    CLOUDFLARE_WORKER_FIELD_NUMBER: _ClassVar[int]
    LAMBDA_FIELD_NUMBER: _ClassVar[int]
    TEMPORAL_FIELD_NUMBER: _ClassVar[int]
    GOLEM_FIELD_NUMBER: _ClassVar[int]
    HATCHET_FIELD_NUMBER: _ClassVar[int]
    SQS_FIELD_NUMBER: _ClassVar[int]
    SNS_FIELD_NUMBER: _ClassVar[int]
    EVENT_BRIDGE_FIELD_NUMBER: _ClassVar[int]
    KAFKA_FIELD_NUMBER: _ClassVar[int]
    GOOGLE_PUB_SUB_FIELD_NUMBER: _ClassVar[int]
    NATS_FIELD_NUMBER: _ClassVar[int]
    SMTP_FIELD_NUMBER: _ClassVar[int]
    RABBIT_MQ_FIELD_NUMBER: _ClassVar[int]
    AZURE_SERVICE_BUS_FIELD_NUMBER: _ClassVar[int]
    REDIS_FIELD_NUMBER: _ClassVar[int]
    LOCAL_FIELD_NUMBER: _ClassVar[int]
    name: str
    display_name: str
    state: Destination.State
    event_types: _containers.RepeatedScalarFieldContainer[Destination.EventType]
    filter: str
    payload_format: Destination.PayloadFormat
    create_time: _timestamp_pb2.Timestamp
    update_time: _timestamp_pb2.Timestamp
    last_test_time: _timestamp_pb2.Timestamp
    last_test_success: bool
    webhook: WebhookTarget
    restate: RestateTarget
    inngest: InngestTarget
    cloudflare_worker: CloudflareWorkerTarget
    temporal: TemporalTarget
    golem: GolemTarget
    hatchet: HatchetTarget
    sqs: SqsTarget
    sns: SnsTarget
    event_bridge: EventBridgeTarget
    kafka: KafkaTarget
    google_pub_sub: GooglePubSubTarget
    nats: NatsTarget
    smtp: SmtpTarget
    rabbit_mq: RabbitMqTarget
    azure_service_bus: AzureServiceBusTarget
    redis: RedisTarget
    local: LocalTarget
    def __init__(self, name: _Optional[str] = ..., display_name: _Optional[str] = ..., state: _Optional[_Union[Destination.State, str]] = ..., event_types: _Optional[_Iterable[_Union[Destination.EventType, str]]] = ..., filter: _Optional[str] = ..., payload_format: _Optional[_Union[Destination.PayloadFormat, str]] = ..., create_time: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., update_time: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., last_test_time: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., last_test_success: _Optional[bool] = ..., webhook: _Optional[_Union[WebhookTarget, _Mapping]] = ..., restate: _Optional[_Union[RestateTarget, _Mapping]] = ..., inngest: _Optional[_Union[InngestTarget, _Mapping]] = ..., cloudflare_worker: _Optional[_Union[CloudflareWorkerTarget, _Mapping]] = ..., temporal: _Optional[_Union[TemporalTarget, _Mapping]] = ..., golem: _Optional[_Union[GolemTarget, _Mapping]] = ..., hatchet: _Optional[_Union[HatchetTarget, _Mapping]] = ..., sqs: _Optional[_Union[SqsTarget, _Mapping]] = ..., sns: _Optional[_Union[SnsTarget, _Mapping]] = ..., event_bridge: _Optional[_Union[EventBridgeTarget, _Mapping]] = ..., kafka: _Optional[_Union[KafkaTarget, _Mapping]] = ..., google_pub_sub: _Optional[_Union[GooglePubSubTarget, _Mapping]] = ..., nats: _Optional[_Union[NatsTarget, _Mapping]] = ..., smtp: _Optional[_Union[SmtpTarget, _Mapping]] = ..., rabbit_mq: _Optional[_Union[RabbitMqTarget, _Mapping]] = ..., azure_service_bus: _Optional[_Union[AzureServiceBusTarget, _Mapping]] = ..., redis: _Optional[_Union[RedisTarget, _Mapping]] = ..., local: _Optional[_Union[LocalTarget, _Mapping]] = ..., **kwargs) -> None: ...

class DeliveryEvent(_message.Message):
    __slots__ = ("delivery_id", "destination", "connector", "message", "delivery_update", "read_receipt", "typing_indicator", "enqueue_time")
    DELIVERY_ID_FIELD_NUMBER: _ClassVar[int]
    DESTINATION_FIELD_NUMBER: _ClassVar[int]
    CONNECTOR_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    DELIVERY_UPDATE_FIELD_NUMBER: _ClassVar[int]
    READ_RECEIPT_FIELD_NUMBER: _ClassVar[int]
    TYPING_INDICATOR_FIELD_NUMBER: _ClassVar[int]
    ENQUEUE_TIME_FIELD_NUMBER: _ClassVar[int]
    delivery_id: str
    destination: str
    connector: str
    message: _message_pb2.Message
    delivery_update: _message_pb2.MessageDelivery
    read_receipt: _message_pb2.ReadReceiptEvent
    typing_indicator: _message_pb2.TypingIndicatorEvent
    enqueue_time: _timestamp_pb2.Timestamp
    def __init__(self, delivery_id: _Optional[str] = ..., destination: _Optional[str] = ..., connector: _Optional[str] = ..., message: _Optional[_Union[_message_pb2.Message, _Mapping]] = ..., delivery_update: _Optional[_Union[_message_pb2.MessageDelivery, _Mapping]] = ..., read_receipt: _Optional[_Union[_message_pb2.ReadReceiptEvent, _Mapping]] = ..., typing_indicator: _Optional[_Union[_message_pb2.TypingIndicatorEvent, _Mapping]] = ..., enqueue_time: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class CreateDestinationRequest(_message.Message):
    __slots__ = ("destination", "request_id", "destination_id")
    DESTINATION_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    DESTINATION_ID_FIELD_NUMBER: _ClassVar[int]
    destination: Destination
    request_id: str
    destination_id: str
    def __init__(self, destination: _Optional[_Union[Destination, _Mapping]] = ..., request_id: _Optional[str] = ..., destination_id: _Optional[str] = ...) -> None: ...

class CreateDestinationResponse(_message.Message):
    __slots__ = ("destination",)
    DESTINATION_FIELD_NUMBER: _ClassVar[int]
    destination: Destination
    def __init__(self, destination: _Optional[_Union[Destination, _Mapping]] = ...) -> None: ...

class GetDestinationRequest(_message.Message):
    __slots__ = ("name",)
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...

class GetDestinationResponse(_message.Message):
    __slots__ = ("destination",)
    DESTINATION_FIELD_NUMBER: _ClassVar[int]
    destination: Destination
    def __init__(self, destination: _Optional[_Union[Destination, _Mapping]] = ...) -> None: ...

class ListDestinationsRequest(_message.Message):
    __slots__ = ("page_size", "page_token", "filter", "order_by")
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    FILTER_FIELD_NUMBER: _ClassVar[int]
    ORDER_BY_FIELD_NUMBER: _ClassVar[int]
    page_size: int
    page_token: str
    filter: str
    order_by: str
    def __init__(self, page_size: _Optional[int] = ..., page_token: _Optional[str] = ..., filter: _Optional[str] = ..., order_by: _Optional[str] = ...) -> None: ...

class ListDestinationsResponse(_message.Message):
    __slots__ = ("destinations", "next_page_token", "total_size")
    DESTINATIONS_FIELD_NUMBER: _ClassVar[int]
    NEXT_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    TOTAL_SIZE_FIELD_NUMBER: _ClassVar[int]
    destinations: _containers.RepeatedCompositeFieldContainer[Destination]
    next_page_token: str
    total_size: int
    def __init__(self, destinations: _Optional[_Iterable[_Union[Destination, _Mapping]]] = ..., next_page_token: _Optional[str] = ..., total_size: _Optional[int] = ...) -> None: ...

class UpdateDestinationRequest(_message.Message):
    __slots__ = ("destination", "update_mask")
    DESTINATION_FIELD_NUMBER: _ClassVar[int]
    UPDATE_MASK_FIELD_NUMBER: _ClassVar[int]
    destination: Destination
    update_mask: _field_mask_pb2.FieldMask
    def __init__(self, destination: _Optional[_Union[Destination, _Mapping]] = ..., update_mask: _Optional[_Union[_field_mask_pb2.FieldMask, _Mapping]] = ...) -> None: ...

class UpdateDestinationResponse(_message.Message):
    __slots__ = ("destination",)
    DESTINATION_FIELD_NUMBER: _ClassVar[int]
    destination: Destination
    def __init__(self, destination: _Optional[_Union[Destination, _Mapping]] = ...) -> None: ...

class DeleteDestinationRequest(_message.Message):
    __slots__ = ("name",)
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...

class DeleteDestinationResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class TestDestinationRequest(_message.Message):
    __slots__ = ("name",)
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...

class TestDestinationResponse(_message.Message):
    __slots__ = ("success", "error_message", "http_status_code", "latency_ms")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    HTTP_STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    LATENCY_MS_FIELD_NUMBER: _ClassVar[int]
    success: bool
    error_message: str
    http_status_code: int
    latency_ms: int
    def __init__(self, success: _Optional[bool] = ..., error_message: _Optional[str] = ..., http_status_code: _Optional[int] = ..., latency_ms: _Optional[int] = ...) -> None: ...

class DestinationTestResult(_message.Message):
    __slots__ = ("success", "error_message", "http_status_code", "latency_ms", "test_time")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    HTTP_STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    LATENCY_MS_FIELD_NUMBER: _ClassVar[int]
    TEST_TIME_FIELD_NUMBER: _ClassVar[int]
    success: bool
    error_message: str
    http_status_code: int
    latency_ms: int
    test_time: _timestamp_pb2.Timestamp
    def __init__(self, success: _Optional[bool] = ..., error_message: _Optional[str] = ..., http_status_code: _Optional[int] = ..., latency_ms: _Optional[int] = ..., test_time: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class ListDestinationTestResultsRequest(_message.Message):
    __slots__ = ("name", "page_size")
    NAME_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    name: str
    page_size: int
    def __init__(self, name: _Optional[str] = ..., page_size: _Optional[int] = ...) -> None: ...

class ListDestinationTestResultsResponse(_message.Message):
    __slots__ = ("results",)
    RESULTS_FIELD_NUMBER: _ClassVar[int]
    results: _containers.RepeatedCompositeFieldContainer[DestinationTestResult]
    def __init__(self, results: _Optional[_Iterable[_Union[DestinationTestResult, _Mapping]]] = ...) -> None: ...

class ValidateDestinationFilterRequest(_message.Message):
    __slots__ = ("filter", "sample_size")
    FILTER_FIELD_NUMBER: _ClassVar[int]
    SAMPLE_SIZE_FIELD_NUMBER: _ClassVar[int]
    filter: str
    sample_size: int
    def __init__(self, filter: _Optional[str] = ..., sample_size: _Optional[int] = ...) -> None: ...

class ValidateDestinationFilterResponse(_message.Message):
    __slots__ = ("valid", "error_message", "matched_count", "total_count")
    VALID_FIELD_NUMBER: _ClassVar[int]
    ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    MATCHED_COUNT_FIELD_NUMBER: _ClassVar[int]
    TOTAL_COUNT_FIELD_NUMBER: _ClassVar[int]
    valid: bool
    error_message: str
    matched_count: int
    total_count: int
    def __init__(self, valid: _Optional[bool] = ..., error_message: _Optional[str] = ..., matched_count: _Optional[int] = ..., total_count: _Optional[int] = ...) -> None: ...

class PollEventsRequest(_message.Message):
    __slots__ = ("name", "cursor", "max_events", "wait_seconds")
    NAME_FIELD_NUMBER: _ClassVar[int]
    CURSOR_FIELD_NUMBER: _ClassVar[int]
    MAX_EVENTS_FIELD_NUMBER: _ClassVar[int]
    WAIT_SECONDS_FIELD_NUMBER: _ClassVar[int]
    name: str
    cursor: str
    max_events: int
    wait_seconds: int
    def __init__(self, name: _Optional[str] = ..., cursor: _Optional[str] = ..., max_events: _Optional[int] = ..., wait_seconds: _Optional[int] = ...) -> None: ...

class PollEventsResponse(_message.Message):
    __slots__ = ("events", "cursor")
    EVENTS_FIELD_NUMBER: _ClassVar[int]
    CURSOR_FIELD_NUMBER: _ClassVar[int]
    events: _containers.RepeatedCompositeFieldContainer[DeliveryEvent]
    cursor: str
    def __init__(self, events: _Optional[_Iterable[_Union[DeliveryEvent, _Mapping]]] = ..., cursor: _Optional[str] = ...) -> None: ...
