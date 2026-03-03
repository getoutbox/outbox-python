import datetime

from buf.validate import validate_pb2 as _validate_pb2
from google.api import client_pb2 as _client_pb2
from google.api import field_behavior_pb2 as _field_behavior_pb2
from google.api import resource_pb2 as _resource_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TemplateStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    TEMPLATE_STATUS_UNSPECIFIED: _ClassVar[TemplateStatus]
    TEMPLATE_STATUS_PENDING: _ClassVar[TemplateStatus]
    TEMPLATE_STATUS_APPROVED: _ClassVar[TemplateStatus]
    TEMPLATE_STATUS_REJECTED: _ClassVar[TemplateStatus]
    TEMPLATE_STATUS_PAUSED: _ClassVar[TemplateStatus]
    TEMPLATE_STATUS_DISABLED: _ClassVar[TemplateStatus]
TEMPLATE_STATUS_UNSPECIFIED: TemplateStatus
TEMPLATE_STATUS_PENDING: TemplateStatus
TEMPLATE_STATUS_APPROVED: TemplateStatus
TEMPLATE_STATUS_REJECTED: TemplateStatus
TEMPLATE_STATUS_PAUSED: TemplateStatus
TEMPLATE_STATUS_DISABLED: TemplateStatus

class Template(_message.Message):
    __slots__ = ("name", "template_name", "language", "category", "components_json", "status", "rejection_reason", "external_id", "create_time", "update_time")
    class Category(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        CATEGORY_UNSPECIFIED: _ClassVar[Template.Category]
        CATEGORY_UTILITY: _ClassVar[Template.Category]
        CATEGORY_MARKETING: _ClassVar[Template.Category]
        CATEGORY_AUTHENTICATION: _ClassVar[Template.Category]
    CATEGORY_UNSPECIFIED: Template.Category
    CATEGORY_UTILITY: Template.Category
    CATEGORY_MARKETING: Template.Category
    CATEGORY_AUTHENTICATION: Template.Category
    NAME_FIELD_NUMBER: _ClassVar[int]
    TEMPLATE_NAME_FIELD_NUMBER: _ClassVar[int]
    LANGUAGE_FIELD_NUMBER: _ClassVar[int]
    CATEGORY_FIELD_NUMBER: _ClassVar[int]
    COMPONENTS_JSON_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    REJECTION_REASON_FIELD_NUMBER: _ClassVar[int]
    EXTERNAL_ID_FIELD_NUMBER: _ClassVar[int]
    CREATE_TIME_FIELD_NUMBER: _ClassVar[int]
    UPDATE_TIME_FIELD_NUMBER: _ClassVar[int]
    name: str
    template_name: str
    language: str
    category: Template.Category
    components_json: str
    status: TemplateStatus
    rejection_reason: str
    external_id: str
    create_time: _timestamp_pb2.Timestamp
    update_time: _timestamp_pb2.Timestamp
    def __init__(self, name: _Optional[str] = ..., template_name: _Optional[str] = ..., language: _Optional[str] = ..., category: _Optional[_Union[Template.Category, str]] = ..., components_json: _Optional[str] = ..., status: _Optional[_Union[TemplateStatus, str]] = ..., rejection_reason: _Optional[str] = ..., external_id: _Optional[str] = ..., create_time: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., update_time: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class CreateTemplateRequest(_message.Message):
    __slots__ = ("parent", "template")
    PARENT_FIELD_NUMBER: _ClassVar[int]
    TEMPLATE_FIELD_NUMBER: _ClassVar[int]
    parent: str
    template: Template
    def __init__(self, parent: _Optional[str] = ..., template: _Optional[_Union[Template, _Mapping]] = ...) -> None: ...

class CreateTemplateResponse(_message.Message):
    __slots__ = ("template",)
    TEMPLATE_FIELD_NUMBER: _ClassVar[int]
    template: Template
    def __init__(self, template: _Optional[_Union[Template, _Mapping]] = ...) -> None: ...

class GetTemplateRequest(_message.Message):
    __slots__ = ("name",)
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...

class GetTemplateResponse(_message.Message):
    __slots__ = ("template",)
    TEMPLATE_FIELD_NUMBER: _ClassVar[int]
    template: Template
    def __init__(self, template: _Optional[_Union[Template, _Mapping]] = ...) -> None: ...

class ListTemplatesRequest(_message.Message):
    __slots__ = ("parent", "page_size", "page_token")
    PARENT_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    parent: str
    page_size: int
    page_token: str
    def __init__(self, parent: _Optional[str] = ..., page_size: _Optional[int] = ..., page_token: _Optional[str] = ...) -> None: ...

class ListTemplatesResponse(_message.Message):
    __slots__ = ("templates", "next_page_token", "total_size")
    TEMPLATES_FIELD_NUMBER: _ClassVar[int]
    NEXT_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    TOTAL_SIZE_FIELD_NUMBER: _ClassVar[int]
    templates: _containers.RepeatedCompositeFieldContainer[Template]
    next_page_token: str
    total_size: int
    def __init__(self, templates: _Optional[_Iterable[_Union[Template, _Mapping]]] = ..., next_page_token: _Optional[str] = ..., total_size: _Optional[int] = ...) -> None: ...

class DeleteTemplateRequest(_message.Message):
    __slots__ = ("name",)
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...

class DeleteTemplateResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
