import datetime

from buf.validate import validate_pb2 as _validate_pb2
from google.api import client_pb2 as _client_pb2
from google.api import field_behavior_pb2 as _field_behavior_pb2
from google.api import field_info_pb2 as _field_info_pb2
from google.api import resource_pb2 as _resource_pb2
from google.protobuf import field_mask_pb2 as _field_mask_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from outbox.v1 import account_pb2 as _account_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MessagePart(_message.Message):
    __slots__ = ("content_type", "disposition", "content", "url", "filename")
    class Disposition(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        DISPOSITION_UNSPECIFIED: _ClassVar[MessagePart.Disposition]
        DISPOSITION_RENDER: _ClassVar[MessagePart.Disposition]
        DISPOSITION_REACTION: _ClassVar[MessagePart.Disposition]
        DISPOSITION_ATTACHMENT: _ClassVar[MessagePart.Disposition]
        DISPOSITION_INLINE: _ClassVar[MessagePart.Disposition]
    DISPOSITION_UNSPECIFIED: MessagePart.Disposition
    DISPOSITION_RENDER: MessagePart.Disposition
    DISPOSITION_REACTION: MessagePart.Disposition
    DISPOSITION_ATTACHMENT: MessagePart.Disposition
    DISPOSITION_INLINE: MessagePart.Disposition
    CONTENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    DISPOSITION_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    URL_FIELD_NUMBER: _ClassVar[int]
    FILENAME_FIELD_NUMBER: _ClassVar[int]
    content_type: str
    disposition: MessagePart.Disposition
    content: bytes
    url: str
    filename: str
    def __init__(self, content_type: _Optional[str] = ..., disposition: _Optional[_Union[MessagePart.Disposition, str]] = ..., content: _Optional[bytes] = ..., url: _Optional[str] = ..., filename: _Optional[str] = ...) -> None: ...

class Message(_message.Message):
    __slots__ = ("name", "direction", "account", "recipient", "parts", "metadata", "reply_to", "group_id", "replaced", "scope", "edit_number", "create_time", "deliver_time", "delete_time")
    class Direction(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        DIRECTION_UNSPECIFIED: _ClassVar[Message.Direction]
        DIRECTION_INBOUND: _ClassVar[Message.Direction]
        DIRECTION_OUTBOUND: _ClassVar[Message.Direction]
    DIRECTION_UNSPECIFIED: Message.Direction
    DIRECTION_INBOUND: Message.Direction
    DIRECTION_OUTBOUND: Message.Direction
    class DeletionScope(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        DELETION_SCOPE_UNSPECIFIED: _ClassVar[Message.DeletionScope]
        DELETION_SCOPE_FOR_SENDER: _ClassVar[Message.DeletionScope]
        DELETION_SCOPE_FOR_EVERYONE: _ClassVar[Message.DeletionScope]
    DELETION_SCOPE_UNSPECIFIED: Message.DeletionScope
    DELETION_SCOPE_FOR_SENDER: Message.DeletionScope
    DELETION_SCOPE_FOR_EVERYONE: Message.DeletionScope
    class MetadataEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    NAME_FIELD_NUMBER: _ClassVar[int]
    DIRECTION_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_FIELD_NUMBER: _ClassVar[int]
    RECIPIENT_FIELD_NUMBER: _ClassVar[int]
    PARTS_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    REPLY_TO_FIELD_NUMBER: _ClassVar[int]
    GROUP_ID_FIELD_NUMBER: _ClassVar[int]
    REPLACED_FIELD_NUMBER: _ClassVar[int]
    SCOPE_FIELD_NUMBER: _ClassVar[int]
    EDIT_NUMBER_FIELD_NUMBER: _ClassVar[int]
    CREATE_TIME_FIELD_NUMBER: _ClassVar[int]
    DELIVER_TIME_FIELD_NUMBER: _ClassVar[int]
    DELETE_TIME_FIELD_NUMBER: _ClassVar[int]
    name: str
    direction: Message.Direction
    account: _account_pb2.Account
    recipient: str
    parts: _containers.RepeatedCompositeFieldContainer[MessagePart]
    metadata: _containers.ScalarMap[str, str]
    reply_to: str
    group_id: str
    replaced: str
    scope: Message.DeletionScope
    edit_number: int
    create_time: _timestamp_pb2.Timestamp
    deliver_time: _timestamp_pb2.Timestamp
    delete_time: _timestamp_pb2.Timestamp
    def __init__(self, name: _Optional[str] = ..., direction: _Optional[_Union[Message.Direction, str]] = ..., account: _Optional[_Union[_account_pb2.Account, _Mapping]] = ..., recipient: _Optional[str] = ..., parts: _Optional[_Iterable[_Union[MessagePart, _Mapping]]] = ..., metadata: _Optional[_Mapping[str, str]] = ..., reply_to: _Optional[str] = ..., group_id: _Optional[str] = ..., replaced: _Optional[str] = ..., scope: _Optional[_Union[Message.DeletionScope, str]] = ..., edit_number: _Optional[int] = ..., create_time: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., deliver_time: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., delete_time: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class MessageDelivery(_message.Message):
    __slots__ = ("account", "message", "status", "error_code", "error_message", "status_change_time")
    class Status(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        STATUS_UNSPECIFIED: _ClassVar[MessageDelivery.Status]
        STATUS_PENDING: _ClassVar[MessageDelivery.Status]
        STATUS_DELIVERED: _ClassVar[MessageDelivery.Status]
        STATUS_DISPLAYED: _ClassVar[MessageDelivery.Status]
        STATUS_PROCESSED: _ClassVar[MessageDelivery.Status]
        STATUS_FAILED: _ClassVar[MessageDelivery.Status]
        STATUS_EXPIRED: _ClassVar[MessageDelivery.Status]
    STATUS_UNSPECIFIED: MessageDelivery.Status
    STATUS_PENDING: MessageDelivery.Status
    STATUS_DELIVERED: MessageDelivery.Status
    STATUS_DISPLAYED: MessageDelivery.Status
    STATUS_PROCESSED: MessageDelivery.Status
    STATUS_FAILED: MessageDelivery.Status
    STATUS_EXPIRED: MessageDelivery.Status
    ACCOUNT_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    ERROR_CODE_FIELD_NUMBER: _ClassVar[int]
    ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    STATUS_CHANGE_TIME_FIELD_NUMBER: _ClassVar[int]
    account: _account_pb2.Account
    message: str
    status: MessageDelivery.Status
    error_code: str
    error_message: str
    status_change_time: _timestamp_pb2.Timestamp
    def __init__(self, account: _Optional[_Union[_account_pb2.Account, _Mapping]] = ..., message: _Optional[str] = ..., status: _Optional[_Union[MessageDelivery.Status, str]] = ..., error_code: _Optional[str] = ..., error_message: _Optional[str] = ..., status_change_time: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class ReadReceiptEvent(_message.Message):
    __slots__ = ("account", "messages", "timestamp")
    ACCOUNT_FIELD_NUMBER: _ClassVar[int]
    MESSAGES_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    account: _account_pb2.Account
    messages: _containers.RepeatedScalarFieldContainer[str]
    timestamp: _timestamp_pb2.Timestamp
    def __init__(self, account: _Optional[_Union[_account_pb2.Account, _Mapping]] = ..., messages: _Optional[_Iterable[str]] = ..., timestamp: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class TypingIndicatorEvent(_message.Message):
    __slots__ = ("account", "typing", "timestamp", "content_type")
    ACCOUNT_FIELD_NUMBER: _ClassVar[int]
    TYPING_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    CONTENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    account: _account_pb2.Account
    typing: bool
    timestamp: _timestamp_pb2.Timestamp
    content_type: str
    def __init__(self, account: _Optional[_Union[_account_pb2.Account, _Mapping]] = ..., typing: _Optional[bool] = ..., timestamp: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., content_type: _Optional[str] = ...) -> None: ...

class CreateMessageRequest(_message.Message):
    __slots__ = ("message", "connector", "request_id")
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    CONNECTOR_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    message: Message
    connector: str
    request_id: str
    def __init__(self, message: _Optional[_Union[Message, _Mapping]] = ..., connector: _Optional[str] = ..., request_id: _Optional[str] = ...) -> None: ...

class CreateMessageResponse(_message.Message):
    __slots__ = ("message", "delivery")
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    DELIVERY_FIELD_NUMBER: _ClassVar[int]
    message: Message
    delivery: MessageDelivery
    def __init__(self, message: _Optional[_Union[Message, _Mapping]] = ..., delivery: _Optional[_Union[MessageDelivery, _Mapping]] = ...) -> None: ...

class UpdateMessageRequest(_message.Message):
    __slots__ = ("message", "update_mask", "request_id")
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    UPDATE_MASK_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    message: Message
    update_mask: _field_mask_pb2.FieldMask
    request_id: str
    def __init__(self, message: _Optional[_Union[Message, _Mapping]] = ..., update_mask: _Optional[_Union[_field_mask_pb2.FieldMask, _Mapping]] = ..., request_id: _Optional[str] = ...) -> None: ...

class UpdateMessageResponse(_message.Message):
    __slots__ = ("message",)
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    message: Message
    def __init__(self, message: _Optional[_Union[Message, _Mapping]] = ...) -> None: ...

class DeleteMessageRequest(_message.Message):
    __slots__ = ("name", "scope", "request_id")
    NAME_FIELD_NUMBER: _ClassVar[int]
    SCOPE_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    name: str
    scope: Message.DeletionScope
    request_id: str
    def __init__(self, name: _Optional[str] = ..., scope: _Optional[_Union[Message.DeletionScope, str]] = ..., request_id: _Optional[str] = ...) -> None: ...

class DeleteMessageResponse(_message.Message):
    __slots__ = ("message",)
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    message: Message
    def __init__(self, message: _Optional[_Union[Message, _Mapping]] = ...) -> None: ...

class SendReadReceiptRequest(_message.Message):
    __slots__ = ("connector", "account", "messages")
    CONNECTOR_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_FIELD_NUMBER: _ClassVar[int]
    MESSAGES_FIELD_NUMBER: _ClassVar[int]
    connector: str
    account: str
    messages: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, connector: _Optional[str] = ..., account: _Optional[str] = ..., messages: _Optional[_Iterable[str]] = ...) -> None: ...

class SendReadReceiptResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class SendTypingIndicatorRequest(_message.Message):
    __slots__ = ("connector", "account", "typing")
    CONNECTOR_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_FIELD_NUMBER: _ClassVar[int]
    TYPING_FIELD_NUMBER: _ClassVar[int]
    connector: str
    account: str
    typing: bool
    def __init__(self, connector: _Optional[str] = ..., account: _Optional[str] = ..., typing: _Optional[bool] = ...) -> None: ...

class SendTypingIndicatorResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ListMessagesRequest(_message.Message):
    __slots__ = ("parent", "page_size", "page_token", "filter", "order_by")
    PARENT_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    FILTER_FIELD_NUMBER: _ClassVar[int]
    ORDER_BY_FIELD_NUMBER: _ClassVar[int]
    parent: str
    page_size: int
    page_token: str
    filter: str
    order_by: str
    def __init__(self, parent: _Optional[str] = ..., page_size: _Optional[int] = ..., page_token: _Optional[str] = ..., filter: _Optional[str] = ..., order_by: _Optional[str] = ...) -> None: ...

class ListMessagesResponse(_message.Message):
    __slots__ = ("messages", "next_page_token", "total_size")
    MESSAGES_FIELD_NUMBER: _ClassVar[int]
    NEXT_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    TOTAL_SIZE_FIELD_NUMBER: _ClassVar[int]
    messages: _containers.RepeatedCompositeFieldContainer[Message]
    next_page_token: str
    total_size: int
    def __init__(self, messages: _Optional[_Iterable[_Union[Message, _Mapping]]] = ..., next_page_token: _Optional[str] = ..., total_size: _Optional[int] = ...) -> None: ...
