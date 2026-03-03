import datetime

from buf.validate import validate_pb2 as _validate_pb2
from google.api import client_pb2 as _client_pb2
from google.api import field_behavior_pb2 as _field_behavior_pb2
from google.api import field_info_pb2 as _field_info_pb2
from google.api import resource_pb2 as _resource_pb2
from google.protobuf import field_mask_pb2 as _field_mask_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from outbox.v1 import account_pb2 as _account_pb2
from outbox.v1 import connector_config_pb2 as _connector_config_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Connector(_message.Message):
    __slots__ = ("name", "account", "state", "tags", "create_time", "update_time", "error_message", "activity_pub", "apns", "apple_messages", "bluesky", "discord", "email", "fcm", "freshchat", "google_chat", "hubspot", "in_app", "instagram", "intercom", "kakao_talk", "lark", "line", "linkedin", "live_chat", "matrix", "mattermost", "messenger", "mqtt", "rcs", "reddit", "signal", "slack", "sms", "teams", "telegram", "threads", "tiktok", "twitch", "viber", "webex", "web_push", "wechat", "whatsapp", "x", "xmpp", "zalo", "zendesk", "zoom_chat")
    class State(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        STATE_UNSPECIFIED: _ClassVar[Connector.State]
        STATE_ACTIVE: _ClassVar[Connector.State]
        STATE_INACTIVE: _ClassVar[Connector.State]
        STATE_AUTHORIZING: _ClassVar[Connector.State]
        STATE_ERROR: _ClassVar[Connector.State]
    STATE_UNSPECIFIED: Connector.State
    STATE_ACTIVE: Connector.State
    STATE_INACTIVE: Connector.State
    STATE_AUTHORIZING: Connector.State
    STATE_ERROR: Connector.State
    NAME_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    CREATE_TIME_FIELD_NUMBER: _ClassVar[int]
    UPDATE_TIME_FIELD_NUMBER: _ClassVar[int]
    ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    ACTIVITY_PUB_FIELD_NUMBER: _ClassVar[int]
    APNS_FIELD_NUMBER: _ClassVar[int]
    APPLE_MESSAGES_FIELD_NUMBER: _ClassVar[int]
    BLUESKY_FIELD_NUMBER: _ClassVar[int]
    DISCORD_FIELD_NUMBER: _ClassVar[int]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    FCM_FIELD_NUMBER: _ClassVar[int]
    FRESHCHAT_FIELD_NUMBER: _ClassVar[int]
    GOOGLE_CHAT_FIELD_NUMBER: _ClassVar[int]
    HUBSPOT_FIELD_NUMBER: _ClassVar[int]
    IN_APP_FIELD_NUMBER: _ClassVar[int]
    INSTAGRAM_FIELD_NUMBER: _ClassVar[int]
    INTERCOM_FIELD_NUMBER: _ClassVar[int]
    KAKAO_TALK_FIELD_NUMBER: _ClassVar[int]
    LARK_FIELD_NUMBER: _ClassVar[int]
    LINE_FIELD_NUMBER: _ClassVar[int]
    LINKEDIN_FIELD_NUMBER: _ClassVar[int]
    LIVE_CHAT_FIELD_NUMBER: _ClassVar[int]
    MATRIX_FIELD_NUMBER: _ClassVar[int]
    MATTERMOST_FIELD_NUMBER: _ClassVar[int]
    MESSENGER_FIELD_NUMBER: _ClassVar[int]
    MQTT_FIELD_NUMBER: _ClassVar[int]
    RCS_FIELD_NUMBER: _ClassVar[int]
    REDDIT_FIELD_NUMBER: _ClassVar[int]
    SIGNAL_FIELD_NUMBER: _ClassVar[int]
    SLACK_FIELD_NUMBER: _ClassVar[int]
    SMS_FIELD_NUMBER: _ClassVar[int]
    TEAMS_FIELD_NUMBER: _ClassVar[int]
    TELEGRAM_FIELD_NUMBER: _ClassVar[int]
    THREADS_FIELD_NUMBER: _ClassVar[int]
    TIKTOK_FIELD_NUMBER: _ClassVar[int]
    TWITCH_FIELD_NUMBER: _ClassVar[int]
    VIBER_FIELD_NUMBER: _ClassVar[int]
    WEBEX_FIELD_NUMBER: _ClassVar[int]
    WEB_PUSH_FIELD_NUMBER: _ClassVar[int]
    WECHAT_FIELD_NUMBER: _ClassVar[int]
    WHATSAPP_FIELD_NUMBER: _ClassVar[int]
    X_FIELD_NUMBER: _ClassVar[int]
    XMPP_FIELD_NUMBER: _ClassVar[int]
    ZALO_FIELD_NUMBER: _ClassVar[int]
    ZENDESK_FIELD_NUMBER: _ClassVar[int]
    ZOOM_CHAT_FIELD_NUMBER: _ClassVar[int]
    name: str
    account: _account_pb2.Account
    state: Connector.State
    tags: _containers.RepeatedScalarFieldContainer[str]
    create_time: _timestamp_pb2.Timestamp
    update_time: _timestamp_pb2.Timestamp
    error_message: str
    activity_pub: _connector_config_pb2.ActivityPubConfig
    apns: _connector_config_pb2.ApnsConfig
    apple_messages: _connector_config_pb2.AppleMessagesConfig
    bluesky: _connector_config_pb2.BlueskyConfig
    discord: _connector_config_pb2.DiscordConfig
    email: _connector_config_pb2.EmailConfig
    fcm: _connector_config_pb2.FcmConfig
    freshchat: _connector_config_pb2.FreshchatConfig
    google_chat: _connector_config_pb2.GoogleChatConfig
    hubspot: _connector_config_pb2.HubspotConfig
    in_app: _connector_config_pb2.InAppConfig
    instagram: _connector_config_pb2.InstagramConfig
    intercom: _connector_config_pb2.IntercomConfig
    kakao_talk: _connector_config_pb2.KakaoTalkConfig
    lark: _connector_config_pb2.LarkConfig
    line: _connector_config_pb2.LineConfig
    linkedin: _connector_config_pb2.LinkedinConfig
    live_chat: _connector_config_pb2.LiveChatConfig
    matrix: _connector_config_pb2.MatrixConfig
    mattermost: _connector_config_pb2.MattermostConfig
    messenger: _connector_config_pb2.MessengerConfig
    mqtt: _connector_config_pb2.MqttConfig
    rcs: _connector_config_pb2.RcsConfig
    reddit: _connector_config_pb2.RedditConfig
    signal: _connector_config_pb2.SignalConfig
    slack: _connector_config_pb2.SlackConfig
    sms: _connector_config_pb2.SmsConfig
    teams: _connector_config_pb2.TeamsConfig
    telegram: _connector_config_pb2.TelegramConfig
    threads: _connector_config_pb2.ThreadsConfig
    tiktok: _connector_config_pb2.TiktokConfig
    twitch: _connector_config_pb2.TwitchConfig
    viber: _connector_config_pb2.ViberConfig
    webex: _connector_config_pb2.WebexConfig
    web_push: _connector_config_pb2.WebPushConfig
    wechat: _connector_config_pb2.WechatConfig
    whatsapp: _connector_config_pb2.WhatsAppConfig
    x: _connector_config_pb2.XConfig
    xmpp: _connector_config_pb2.XmppConfig
    zalo: _connector_config_pb2.ZaloConfig
    zendesk: _connector_config_pb2.ZendeskConfig
    zoom_chat: _connector_config_pb2.ZoomChatConfig
    def __init__(self, name: _Optional[str] = ..., account: _Optional[_Union[_account_pb2.Account, _Mapping]] = ..., state: _Optional[_Union[Connector.State, str]] = ..., tags: _Optional[_Iterable[str]] = ..., create_time: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., update_time: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., error_message: _Optional[str] = ..., activity_pub: _Optional[_Union[_connector_config_pb2.ActivityPubConfig, _Mapping]] = ..., apns: _Optional[_Union[_connector_config_pb2.ApnsConfig, _Mapping]] = ..., apple_messages: _Optional[_Union[_connector_config_pb2.AppleMessagesConfig, _Mapping]] = ..., bluesky: _Optional[_Union[_connector_config_pb2.BlueskyConfig, _Mapping]] = ..., discord: _Optional[_Union[_connector_config_pb2.DiscordConfig, _Mapping]] = ..., email: _Optional[_Union[_connector_config_pb2.EmailConfig, _Mapping]] = ..., fcm: _Optional[_Union[_connector_config_pb2.FcmConfig, _Mapping]] = ..., freshchat: _Optional[_Union[_connector_config_pb2.FreshchatConfig, _Mapping]] = ..., google_chat: _Optional[_Union[_connector_config_pb2.GoogleChatConfig, _Mapping]] = ..., hubspot: _Optional[_Union[_connector_config_pb2.HubspotConfig, _Mapping]] = ..., in_app: _Optional[_Union[_connector_config_pb2.InAppConfig, _Mapping]] = ..., instagram: _Optional[_Union[_connector_config_pb2.InstagramConfig, _Mapping]] = ..., intercom: _Optional[_Union[_connector_config_pb2.IntercomConfig, _Mapping]] = ..., kakao_talk: _Optional[_Union[_connector_config_pb2.KakaoTalkConfig, _Mapping]] = ..., lark: _Optional[_Union[_connector_config_pb2.LarkConfig, _Mapping]] = ..., line: _Optional[_Union[_connector_config_pb2.LineConfig, _Mapping]] = ..., linkedin: _Optional[_Union[_connector_config_pb2.LinkedinConfig, _Mapping]] = ..., live_chat: _Optional[_Union[_connector_config_pb2.LiveChatConfig, _Mapping]] = ..., matrix: _Optional[_Union[_connector_config_pb2.MatrixConfig, _Mapping]] = ..., mattermost: _Optional[_Union[_connector_config_pb2.MattermostConfig, _Mapping]] = ..., messenger: _Optional[_Union[_connector_config_pb2.MessengerConfig, _Mapping]] = ..., mqtt: _Optional[_Union[_connector_config_pb2.MqttConfig, _Mapping]] = ..., rcs: _Optional[_Union[_connector_config_pb2.RcsConfig, _Mapping]] = ..., reddit: _Optional[_Union[_connector_config_pb2.RedditConfig, _Mapping]] = ..., signal: _Optional[_Union[_connector_config_pb2.SignalConfig, _Mapping]] = ..., slack: _Optional[_Union[_connector_config_pb2.SlackConfig, _Mapping]] = ..., sms: _Optional[_Union[_connector_config_pb2.SmsConfig, _Mapping]] = ..., teams: _Optional[_Union[_connector_config_pb2.TeamsConfig, _Mapping]] = ..., telegram: _Optional[_Union[_connector_config_pb2.TelegramConfig, _Mapping]] = ..., threads: _Optional[_Union[_connector_config_pb2.ThreadsConfig, _Mapping]] = ..., tiktok: _Optional[_Union[_connector_config_pb2.TiktokConfig, _Mapping]] = ..., twitch: _Optional[_Union[_connector_config_pb2.TwitchConfig, _Mapping]] = ..., viber: _Optional[_Union[_connector_config_pb2.ViberConfig, _Mapping]] = ..., webex: _Optional[_Union[_connector_config_pb2.WebexConfig, _Mapping]] = ..., web_push: _Optional[_Union[_connector_config_pb2.WebPushConfig, _Mapping]] = ..., wechat: _Optional[_Union[_connector_config_pb2.WechatConfig, _Mapping]] = ..., whatsapp: _Optional[_Union[_connector_config_pb2.WhatsAppConfig, _Mapping]] = ..., x: _Optional[_Union[_connector_config_pb2.XConfig, _Mapping]] = ..., xmpp: _Optional[_Union[_connector_config_pb2.XmppConfig, _Mapping]] = ..., zalo: _Optional[_Union[_connector_config_pb2.ZaloConfig, _Mapping]] = ..., zendesk: _Optional[_Union[_connector_config_pb2.ZendeskConfig, _Mapping]] = ..., zoom_chat: _Optional[_Union[_connector_config_pb2.ZoomChatConfig, _Mapping]] = ...) -> None: ...

class CreateConnectorRequest(_message.Message):
    __slots__ = ("connector", "request_id")
    CONNECTOR_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    connector: Connector
    request_id: str
    def __init__(self, connector: _Optional[_Union[Connector, _Mapping]] = ..., request_id: _Optional[str] = ...) -> None: ...

class CreateConnectorResponse(_message.Message):
    __slots__ = ("connector", "authorization_url")
    CONNECTOR_FIELD_NUMBER: _ClassVar[int]
    AUTHORIZATION_URL_FIELD_NUMBER: _ClassVar[int]
    connector: Connector
    authorization_url: str
    def __init__(self, connector: _Optional[_Union[Connector, _Mapping]] = ..., authorization_url: _Optional[str] = ...) -> None: ...

class GetConnectorRequest(_message.Message):
    __slots__ = ("name",)
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...

class GetConnectorResponse(_message.Message):
    __slots__ = ("connector",)
    CONNECTOR_FIELD_NUMBER: _ClassVar[int]
    connector: Connector
    def __init__(self, connector: _Optional[_Union[Connector, _Mapping]] = ...) -> None: ...

class ListConnectorsRequest(_message.Message):
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

class ListConnectorsResponse(_message.Message):
    __slots__ = ("connectors", "next_page_token", "total_size")
    CONNECTORS_FIELD_NUMBER: _ClassVar[int]
    NEXT_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    TOTAL_SIZE_FIELD_NUMBER: _ClassVar[int]
    connectors: _containers.RepeatedCompositeFieldContainer[Connector]
    next_page_token: str
    total_size: int
    def __init__(self, connectors: _Optional[_Iterable[_Union[Connector, _Mapping]]] = ..., next_page_token: _Optional[str] = ..., total_size: _Optional[int] = ...) -> None: ...

class UpdateConnectorRequest(_message.Message):
    __slots__ = ("connector", "update_mask")
    CONNECTOR_FIELD_NUMBER: _ClassVar[int]
    UPDATE_MASK_FIELD_NUMBER: _ClassVar[int]
    connector: Connector
    update_mask: _field_mask_pb2.FieldMask
    def __init__(self, connector: _Optional[_Union[Connector, _Mapping]] = ..., update_mask: _Optional[_Union[_field_mask_pb2.FieldMask, _Mapping]] = ...) -> None: ...

class UpdateConnectorResponse(_message.Message):
    __slots__ = ("connector",)
    CONNECTOR_FIELD_NUMBER: _ClassVar[int]
    connector: Connector
    def __init__(self, connector: _Optional[_Union[Connector, _Mapping]] = ...) -> None: ...

class DeleteConnectorRequest(_message.Message):
    __slots__ = ("name",)
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...

class DeleteConnectorResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ActivateConnectorRequest(_message.Message):
    __slots__ = ("name",)
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...

class ActivateConnectorResponse(_message.Message):
    __slots__ = ("connector",)
    CONNECTOR_FIELD_NUMBER: _ClassVar[int]
    connector: Connector
    def __init__(self, connector: _Optional[_Union[Connector, _Mapping]] = ...) -> None: ...

class DeactivateConnectorRequest(_message.Message):
    __slots__ = ("name",)
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...

class DeactivateConnectorResponse(_message.Message):
    __slots__ = ("connector",)
    CONNECTOR_FIELD_NUMBER: _ClassVar[int]
    connector: Connector
    def __init__(self, connector: _Optional[_Union[Connector, _Mapping]] = ...) -> None: ...

class ReauthorizeConnectorRequest(_message.Message):
    __slots__ = ("name",)
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...

class ReauthorizeConnectorResponse(_message.Message):
    __slots__ = ("authorization_url",)
    AUTHORIZATION_URL_FIELD_NUMBER: _ClassVar[int]
    authorization_url: str
    def __init__(self, authorization_url: _Optional[str] = ...) -> None: ...
