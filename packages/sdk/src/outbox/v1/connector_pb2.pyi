import datetime

from buf.validate import validate_pb2 as _validate_pb2
from google.api import client_pb2 as _client_pb2
from google.api import field_behavior_pb2 as _field_behavior_pb2
from google.api import field_info_pb2 as _field_info_pb2
from google.api import resource_pb2 as _resource_pb2
from google.longrunning import operations_pb2 as _operations_pb2
from google.protobuf import field_mask_pb2 as _field_mask_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ProvisionedResourceState(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    PROVISIONED_RESOURCE_STATE_UNSPECIFIED: _ClassVar[ProvisionedResourceState]
    PROVISIONED_RESOURCE_STATE_PENDING: _ClassVar[ProvisionedResourceState]
    PROVISIONED_RESOURCE_STATE_PROVISIONING: _ClassVar[ProvisionedResourceState]
    PROVISIONED_RESOURCE_STATE_ACTIVE: _ClassVar[ProvisionedResourceState]
    PROVISIONED_RESOURCE_STATE_SUSPENDED: _ClassVar[ProvisionedResourceState]
    PROVISIONED_RESOURCE_STATE_RELEASED: _ClassVar[ProvisionedResourceState]
    PROVISIONED_RESOURCE_STATE_FAILED: _ClassVar[ProvisionedResourceState]
    PROVISIONED_RESOURCE_STATE_CANCELLING: _ClassVar[ProvisionedResourceState]
    PROVISIONED_RESOURCE_STATE_PORTING: _ClassVar[ProvisionedResourceState]
    PROVISIONED_RESOURCE_STATE_PORT_FAILED: _ClassVar[ProvisionedResourceState]

class ConnectorKind(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CONNECTOR_KIND_UNSPECIFIED: _ClassVar[ConnectorKind]
    CONNECTOR_KIND_MANAGED: _ClassVar[ConnectorKind]
    CONNECTOR_KIND_USER: _ClassVar[ConnectorKind]
    CONNECTOR_KIND_BOT: _ClassVar[ConnectorKind]

class ConnectorState(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CONNECTOR_STATE_UNSPECIFIED: _ClassVar[ConnectorState]
    CONNECTOR_STATE_ACTIVE: _ClassVar[ConnectorState]
    CONNECTOR_STATE_INACTIVE: _ClassVar[ConnectorState]
    CONNECTOR_STATE_AUTHORIZING: _ClassVar[ConnectorState]
    CONNECTOR_STATE_ERROR: _ClassVar[ConnectorState]

class ConnectorReadiness(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CONNECTOR_READINESS_UNSPECIFIED: _ClassVar[ConnectorReadiness]
    CONNECTOR_READINESS_READY: _ClassVar[ConnectorReadiness]
    CONNECTOR_READINESS_PENDING_COMPLIANCE: _ClassVar[ConnectorReadiness]
    CONNECTOR_READINESS_RESOURCE_NOT_ACTIVE: _ClassVar[ConnectorReadiness]
    CONNECTOR_READINESS_RESOURCE_SUSPENDED: _ClassVar[ConnectorReadiness]
PROVISIONED_RESOURCE_STATE_UNSPECIFIED: ProvisionedResourceState
PROVISIONED_RESOURCE_STATE_PENDING: ProvisionedResourceState
PROVISIONED_RESOURCE_STATE_PROVISIONING: ProvisionedResourceState
PROVISIONED_RESOURCE_STATE_ACTIVE: ProvisionedResourceState
PROVISIONED_RESOURCE_STATE_SUSPENDED: ProvisionedResourceState
PROVISIONED_RESOURCE_STATE_RELEASED: ProvisionedResourceState
PROVISIONED_RESOURCE_STATE_FAILED: ProvisionedResourceState
PROVISIONED_RESOURCE_STATE_CANCELLING: ProvisionedResourceState
PROVISIONED_RESOURCE_STATE_PORTING: ProvisionedResourceState
PROVISIONED_RESOURCE_STATE_PORT_FAILED: ProvisionedResourceState
CONNECTOR_KIND_UNSPECIFIED: ConnectorKind
CONNECTOR_KIND_MANAGED: ConnectorKind
CONNECTOR_KIND_USER: ConnectorKind
CONNECTOR_KIND_BOT: ConnectorKind
CONNECTOR_STATE_UNSPECIFIED: ConnectorState
CONNECTOR_STATE_ACTIVE: ConnectorState
CONNECTOR_STATE_INACTIVE: ConnectorState
CONNECTOR_STATE_AUTHORIZING: ConnectorState
CONNECTOR_STATE_ERROR: ConnectorState
CONNECTOR_READINESS_UNSPECIFIED: ConnectorReadiness
CONNECTOR_READINESS_READY: ConnectorReadiness
CONNECTOR_READINESS_PENDING_COMPLIANCE: ConnectorReadiness
CONNECTOR_READINESS_RESOURCE_NOT_ACTIVE: ConnectorReadiness
CONNECTOR_READINESS_RESOURCE_SUSPENDED: ConnectorReadiness

class OutboxSmsConfig(_message.Message):
    __slots__ = ("country", "area_code")
    COUNTRY_FIELD_NUMBER: _ClassVar[int]
    AREA_CODE_FIELD_NUMBER: _ClassVar[int]
    country: str
    area_code: str
    def __init__(self, country: _Optional[str] = ..., area_code: _Optional[str] = ...) -> None: ...

class OutboxRcsConfig(_message.Message):
    __slots__ = ("country", "brand_name")
    COUNTRY_FIELD_NUMBER: _ClassVar[int]
    BRAND_NAME_FIELD_NUMBER: _ClassVar[int]
    country: str
    brand_name: str
    def __init__(self, country: _Optional[str] = ..., brand_name: _Optional[str] = ...) -> None: ...

class OutboxWhatsAppConfig(_message.Message):
    __slots__ = ("display_name", "business_name")
    DISPLAY_NAME_FIELD_NUMBER: _ClassVar[int]
    BUSINESS_NAME_FIELD_NUMBER: _ClassVar[int]
    display_name: str
    business_name: str
    def __init__(self, display_name: _Optional[str] = ..., business_name: _Optional[str] = ...) -> None: ...

class OutboxEmailConfig(_message.Message):
    __slots__ = ("address", "from_name", "dns_records")
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    FROM_NAME_FIELD_NUMBER: _ClassVar[int]
    DNS_RECORDS_FIELD_NUMBER: _ClassVar[int]
    address: str
    from_name: str
    dns_records: _containers.RepeatedCompositeFieldContainer[DnsRecord]
    def __init__(self, address: _Optional[str] = ..., from_name: _Optional[str] = ..., dns_records: _Optional[_Iterable[_Union[DnsRecord, _Mapping]]] = ...) -> None: ...

class DnsRecord(_message.Message):
    __slots__ = ("type", "name", "value", "priority", "note")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    PRIORITY_FIELD_NUMBER: _ClassVar[int]
    NOTE_FIELD_NUMBER: _ClassVar[int]
    type: str
    name: str
    value: str
    priority: int
    note: str
    def __init__(self, type: _Optional[str] = ..., name: _Optional[str] = ..., value: _Optional[str] = ..., priority: _Optional[int] = ..., note: _Optional[str] = ...) -> None: ...

class TelegramBotConfig(_message.Message):
    __slots__ = ("bot_token",)
    BOT_TOKEN_FIELD_NUMBER: _ClassVar[int]
    bot_token: str
    def __init__(self, bot_token: _Optional[str] = ...) -> None: ...

class DiscordBotConfig(_message.Message):
    __slots__ = ("bot_token",)
    BOT_TOKEN_FIELD_NUMBER: _ClassVar[int]
    bot_token: str
    def __init__(self, bot_token: _Optional[str] = ...) -> None: ...

class SlackBotConfig(_message.Message):
    __slots__ = ("bot_token", "signing_secret")
    BOT_TOKEN_FIELD_NUMBER: _ClassVar[int]
    SIGNING_SECRET_FIELD_NUMBER: _ClassVar[int]
    bot_token: str
    signing_secret: str
    def __init__(self, bot_token: _Optional[str] = ..., signing_secret: _Optional[str] = ...) -> None: ...

class SlackOAuthConfig(_message.Message):
    __slots__ = ("client_id", "client_secret", "signing_secret")
    CLIENT_ID_FIELD_NUMBER: _ClassVar[int]
    CLIENT_SECRET_FIELD_NUMBER: _ClassVar[int]
    SIGNING_SECRET_FIELD_NUMBER: _ClassVar[int]
    client_id: str
    client_secret: str
    signing_secret: str
    def __init__(self, client_id: _Optional[str] = ..., client_secret: _Optional[str] = ..., signing_secret: _Optional[str] = ...) -> None: ...

class TeamsBotConfig(_message.Message):
    __slots__ = ("tenant_id", "client_id", "client_secret")
    TENANT_ID_FIELD_NUMBER: _ClassVar[int]
    CLIENT_ID_FIELD_NUMBER: _ClassVar[int]
    CLIENT_SECRET_FIELD_NUMBER: _ClassVar[int]
    tenant_id: str
    client_id: str
    client_secret: str
    def __init__(self, tenant_id: _Optional[str] = ..., client_id: _Optional[str] = ..., client_secret: _Optional[str] = ...) -> None: ...

class MessengerBotConfig(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class InstagramBotConfig(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ViberBotConfig(_message.Message):
    __slots__ = ("auth_token",)
    AUTH_TOKEN_FIELD_NUMBER: _ClassVar[int]
    auth_token: str
    def __init__(self, auth_token: _Optional[str] = ...) -> None: ...

class LineBotConfig(_message.Message):
    __slots__ = ("channel_token", "channel_secret")
    CHANNEL_TOKEN_FIELD_NUMBER: _ClassVar[int]
    CHANNEL_SECRET_FIELD_NUMBER: _ClassVar[int]
    channel_token: str
    channel_secret: str
    def __init__(self, channel_token: _Optional[str] = ..., channel_secret: _Optional[str] = ...) -> None: ...

class LineOAuthConfig(_message.Message):
    __slots__ = ("client_id", "client_secret")
    CLIENT_ID_FIELD_NUMBER: _ClassVar[int]
    CLIENT_SECRET_FIELD_NUMBER: _ClassVar[int]
    client_id: str
    client_secret: str
    def __init__(self, client_id: _Optional[str] = ..., client_secret: _Optional[str] = ...) -> None: ...

class WeChatBotConfig(_message.Message):
    __slots__ = ("app_id", "app_secret", "token")
    APP_ID_FIELD_NUMBER: _ClassVar[int]
    APP_SECRET_FIELD_NUMBER: _ClassVar[int]
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    app_id: str
    app_secret: str
    token: str
    def __init__(self, app_id: _Optional[str] = ..., app_secret: _Optional[str] = ..., token: _Optional[str] = ...) -> None: ...

class KakaoTalkBotConfig(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class LarkBotConfig(_message.Message):
    __slots__ = ("app_id", "app_secret")
    APP_ID_FIELD_NUMBER: _ClassVar[int]
    APP_SECRET_FIELD_NUMBER: _ClassVar[int]
    app_id: str
    app_secret: str
    def __init__(self, app_id: _Optional[str] = ..., app_secret: _Optional[str] = ...) -> None: ...

class GoogleChatBotConfig(_message.Message):
    __slots__ = ("service_account_key",)
    SERVICE_ACCOUNT_KEY_FIELD_NUMBER: _ClassVar[int]
    service_account_key: str
    def __init__(self, service_account_key: _Optional[str] = ...) -> None: ...

class ZoomChatS2SConfig(_message.Message):
    __slots__ = ("client_id", "client_secret", "account_id")
    CLIENT_ID_FIELD_NUMBER: _ClassVar[int]
    CLIENT_SECRET_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    client_id: str
    client_secret: str
    account_id: str
    def __init__(self, client_id: _Optional[str] = ..., client_secret: _Optional[str] = ..., account_id: _Optional[str] = ...) -> None: ...

class WebexBotConfig(_message.Message):
    __slots__ = ("bot_token",)
    BOT_TOKEN_FIELD_NUMBER: _ClassVar[int]
    bot_token: str
    def __init__(self, bot_token: _Optional[str] = ...) -> None: ...

class MattermostBotConfig(_message.Message):
    __slots__ = ("url", "bot_token")
    URL_FIELD_NUMBER: _ClassVar[int]
    BOT_TOKEN_FIELD_NUMBER: _ClassVar[int]
    url: str
    bot_token: str
    def __init__(self, url: _Optional[str] = ..., bot_token: _Optional[str] = ...) -> None: ...

class ZendeskConfig(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class HubspotConfig(_message.Message):
    __slots__ = ("client_id", "client_secret")
    CLIENT_ID_FIELD_NUMBER: _ClassVar[int]
    CLIENT_SECRET_FIELD_NUMBER: _ClassVar[int]
    client_id: str
    client_secret: str
    def __init__(self, client_id: _Optional[str] = ..., client_secret: _Optional[str] = ...) -> None: ...

class IntercomConfig(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class FreshchatConfig(_message.Message):
    __slots__ = ("app_id", "api_token")
    APP_ID_FIELD_NUMBER: _ClassVar[int]
    API_TOKEN_FIELD_NUMBER: _ClassVar[int]
    app_id: str
    api_token: str
    def __init__(self, app_id: _Optional[str] = ..., api_token: _Optional[str] = ...) -> None: ...

class LiveChatConfig(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class InAppConfig(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class XBotConfig(_message.Message):
    __slots__ = ("bearer_token",)
    BEARER_TOKEN_FIELD_NUMBER: _ClassVar[int]
    bearer_token: str
    def __init__(self, bearer_token: _Optional[str] = ...) -> None: ...

class LinkedInCompanyConfig(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class RedditBotConfig(_message.Message):
    __slots__ = ("client_id", "client_secret", "username", "password")
    CLIENT_ID_FIELD_NUMBER: _ClassVar[int]
    CLIENT_SECRET_FIELD_NUMBER: _ClassVar[int]
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    client_id: str
    client_secret: str
    username: str
    password: str
    def __init__(self, client_id: _Optional[str] = ..., client_secret: _Optional[str] = ..., username: _Optional[str] = ..., password: _Optional[str] = ...) -> None: ...

class TikTokBotConfig(_message.Message):
    __slots__ = ("client_key", "client_secret")
    CLIENT_KEY_FIELD_NUMBER: _ClassVar[int]
    CLIENT_SECRET_FIELD_NUMBER: _ClassVar[int]
    client_key: str
    client_secret: str
    def __init__(self, client_key: _Optional[str] = ..., client_secret: _Optional[str] = ...) -> None: ...

class TwitchBotConfig(_message.Message):
    __slots__ = ("client_id", "client_secret", "sender_user_id")
    CLIENT_ID_FIELD_NUMBER: _ClassVar[int]
    CLIENT_SECRET_FIELD_NUMBER: _ClassVar[int]
    SENDER_USER_ID_FIELD_NUMBER: _ClassVar[int]
    client_id: str
    client_secret: str
    sender_user_id: str
    def __init__(self, client_id: _Optional[str] = ..., client_secret: _Optional[str] = ..., sender_user_id: _Optional[str] = ...) -> None: ...

class BlueskyBotConfig(_message.Message):
    __slots__ = ("handle", "app_password")
    HANDLE_FIELD_NUMBER: _ClassVar[int]
    APP_PASSWORD_FIELD_NUMBER: _ClassVar[int]
    handle: str
    app_password: str
    def __init__(self, handle: _Optional[str] = ..., app_password: _Optional[str] = ...) -> None: ...

class ActivityPubBotConfig(_message.Message):
    __slots__ = ("actor_url", "private_key")
    ACTOR_URL_FIELD_NUMBER: _ClassVar[int]
    PRIVATE_KEY_FIELD_NUMBER: _ClassVar[int]
    actor_url: str
    private_key: str
    def __init__(self, actor_url: _Optional[str] = ..., private_key: _Optional[str] = ...) -> None: ...

class AppleMessagesConfig(_message.Message):
    __slots__ = ("business_id", "msp_id")
    BUSINESS_ID_FIELD_NUMBER: _ClassVar[int]
    MSP_ID_FIELD_NUMBER: _ClassVar[int]
    business_id: str
    msp_id: str
    def __init__(self, business_id: _Optional[str] = ..., msp_id: _Optional[str] = ...) -> None: ...

class WhatsAppBotConfig(_message.Message):
    __slots__ = ("app_id", "app_secret")
    APP_ID_FIELD_NUMBER: _ClassVar[int]
    APP_SECRET_FIELD_NUMBER: _ClassVar[int]
    app_id: str
    app_secret: str
    def __init__(self, app_id: _Optional[str] = ..., app_secret: _Optional[str] = ...) -> None: ...

class TelegramUserConfig(_message.Message):
    __slots__ = ("phone", "api_id", "api_hash", "session_string")
    PHONE_FIELD_NUMBER: _ClassVar[int]
    API_ID_FIELD_NUMBER: _ClassVar[int]
    API_HASH_FIELD_NUMBER: _ClassVar[int]
    SESSION_STRING_FIELD_NUMBER: _ClassVar[int]
    phone: str
    api_id: str
    api_hash: str
    session_string: str
    def __init__(self, phone: _Optional[str] = ..., api_id: _Optional[str] = ..., api_hash: _Optional[str] = ..., session_string: _Optional[str] = ...) -> None: ...

class XUserConfig(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class LinkedInUserConfig(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class RedditUserConfig(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class BlueskyUserConfig(_message.Message):
    __slots__ = ("handle", "app_password")
    HANDLE_FIELD_NUMBER: _ClassVar[int]
    APP_PASSWORD_FIELD_NUMBER: _ClassVar[int]
    handle: str
    app_password: str
    def __init__(self, handle: _Optional[str] = ..., app_password: _Optional[str] = ...) -> None: ...

class TikTokUserConfig(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class TwitchUserConfig(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GoogleChatUserConfig(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ZoomChatUserConfig(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class WebexUserConfig(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class LarkUserConfig(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class SignalUserConfig(_message.Message):
    __slots__ = ("phone_number",)
    PHONE_NUMBER_FIELD_NUMBER: _ClassVar[int]
    phone_number: str
    def __init__(self, phone_number: _Optional[str] = ...) -> None: ...

class ActivityPubUserConfig(_message.Message):
    __slots__ = ("actor_url", "private_key")
    ACTOR_URL_FIELD_NUMBER: _ClassVar[int]
    PRIVATE_KEY_FIELD_NUMBER: _ClassVar[int]
    actor_url: str
    private_key: str
    def __init__(self, actor_url: _Optional[str] = ..., private_key: _Optional[str] = ...) -> None: ...

class MatrixUserConfig(_message.Message):
    __slots__ = ("homeserver_url", "access_token")
    HOMESERVER_URL_FIELD_NUMBER: _ClassVar[int]
    ACCESS_TOKEN_FIELD_NUMBER: _ClassVar[int]
    homeserver_url: str
    access_token: str
    def __init__(self, homeserver_url: _Optional[str] = ..., access_token: _Optional[str] = ...) -> None: ...

class XmppUserConfig(_message.Message):
    __slots__ = ("server", "username", "password")
    SERVER_FIELD_NUMBER: _ClassVar[int]
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    server: str
    username: str
    password: str
    def __init__(self, server: _Optional[str] = ..., username: _Optional[str] = ..., password: _Optional[str] = ...) -> None: ...

class MattermostUserConfig(_message.Message):
    __slots__ = ("url", "personal_access_token")
    URL_FIELD_NUMBER: _ClassVar[int]
    PERSONAL_ACCESS_TOKEN_FIELD_NUMBER: _ClassVar[int]
    url: str
    personal_access_token: str
    def __init__(self, url: _Optional[str] = ..., personal_access_token: _Optional[str] = ...) -> None: ...

class Connector(_message.Message):
    __slots__ = ("name", "kind", "state", "readiness", "provisioned_resources", "webhook_url", "tags", "error_message", "create_time", "update_time", "display_name", "outbox_sms", "outbox_rcs", "outbox_whatsapp", "outbox_email", "telegram_bot", "discord_bot", "slack_bot", "slack_oauth", "teams_bot", "messenger_bot", "instagram_bot", "viber_bot", "line_bot", "line_oauth", "wechat_bot", "kakao_talk_bot", "lark_bot", "google_chat_bot", "zoom_chat_s2s", "webex_bot", "mattermost_bot", "zendesk", "hubspot", "intercom", "freshchat", "live_chat", "in_app", "x_bot", "linkedin_company", "reddit_bot", "tiktok_bot", "twitch_bot", "bluesky_bot", "activity_pub_bot", "apple_messages", "whatsapp_bot", "telegram_user", "x_user", "linkedin_user", "reddit_user", "bluesky_user", "tiktok_user", "twitch_user", "google_chat_user", "zoom_chat_user", "webex_user", "lark_user", "signal_user", "activity_pub_user", "matrix_user", "xmpp_user", "mattermost_user")
    NAME_FIELD_NUMBER: _ClassVar[int]
    KIND_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    READINESS_FIELD_NUMBER: _ClassVar[int]
    PROVISIONED_RESOURCES_FIELD_NUMBER: _ClassVar[int]
    WEBHOOK_URL_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    CREATE_TIME_FIELD_NUMBER: _ClassVar[int]
    UPDATE_TIME_FIELD_NUMBER: _ClassVar[int]
    DISPLAY_NAME_FIELD_NUMBER: _ClassVar[int]
    OUTBOX_SMS_FIELD_NUMBER: _ClassVar[int]
    OUTBOX_RCS_FIELD_NUMBER: _ClassVar[int]
    OUTBOX_WHATSAPP_FIELD_NUMBER: _ClassVar[int]
    OUTBOX_EMAIL_FIELD_NUMBER: _ClassVar[int]
    TELEGRAM_BOT_FIELD_NUMBER: _ClassVar[int]
    DISCORD_BOT_FIELD_NUMBER: _ClassVar[int]
    SLACK_BOT_FIELD_NUMBER: _ClassVar[int]
    SLACK_OAUTH_FIELD_NUMBER: _ClassVar[int]
    TEAMS_BOT_FIELD_NUMBER: _ClassVar[int]
    MESSENGER_BOT_FIELD_NUMBER: _ClassVar[int]
    INSTAGRAM_BOT_FIELD_NUMBER: _ClassVar[int]
    VIBER_BOT_FIELD_NUMBER: _ClassVar[int]
    LINE_BOT_FIELD_NUMBER: _ClassVar[int]
    LINE_OAUTH_FIELD_NUMBER: _ClassVar[int]
    WECHAT_BOT_FIELD_NUMBER: _ClassVar[int]
    KAKAO_TALK_BOT_FIELD_NUMBER: _ClassVar[int]
    LARK_BOT_FIELD_NUMBER: _ClassVar[int]
    GOOGLE_CHAT_BOT_FIELD_NUMBER: _ClassVar[int]
    ZOOM_CHAT_S2S_FIELD_NUMBER: _ClassVar[int]
    WEBEX_BOT_FIELD_NUMBER: _ClassVar[int]
    MATTERMOST_BOT_FIELD_NUMBER: _ClassVar[int]
    ZENDESK_FIELD_NUMBER: _ClassVar[int]
    HUBSPOT_FIELD_NUMBER: _ClassVar[int]
    INTERCOM_FIELD_NUMBER: _ClassVar[int]
    FRESHCHAT_FIELD_NUMBER: _ClassVar[int]
    LIVE_CHAT_FIELD_NUMBER: _ClassVar[int]
    IN_APP_FIELD_NUMBER: _ClassVar[int]
    X_BOT_FIELD_NUMBER: _ClassVar[int]
    LINKEDIN_COMPANY_FIELD_NUMBER: _ClassVar[int]
    REDDIT_BOT_FIELD_NUMBER: _ClassVar[int]
    TIKTOK_BOT_FIELD_NUMBER: _ClassVar[int]
    TWITCH_BOT_FIELD_NUMBER: _ClassVar[int]
    BLUESKY_BOT_FIELD_NUMBER: _ClassVar[int]
    ACTIVITY_PUB_BOT_FIELD_NUMBER: _ClassVar[int]
    APPLE_MESSAGES_FIELD_NUMBER: _ClassVar[int]
    WHATSAPP_BOT_FIELD_NUMBER: _ClassVar[int]
    TELEGRAM_USER_FIELD_NUMBER: _ClassVar[int]
    X_USER_FIELD_NUMBER: _ClassVar[int]
    LINKEDIN_USER_FIELD_NUMBER: _ClassVar[int]
    REDDIT_USER_FIELD_NUMBER: _ClassVar[int]
    BLUESKY_USER_FIELD_NUMBER: _ClassVar[int]
    TIKTOK_USER_FIELD_NUMBER: _ClassVar[int]
    TWITCH_USER_FIELD_NUMBER: _ClassVar[int]
    GOOGLE_CHAT_USER_FIELD_NUMBER: _ClassVar[int]
    ZOOM_CHAT_USER_FIELD_NUMBER: _ClassVar[int]
    WEBEX_USER_FIELD_NUMBER: _ClassVar[int]
    LARK_USER_FIELD_NUMBER: _ClassVar[int]
    SIGNAL_USER_FIELD_NUMBER: _ClassVar[int]
    ACTIVITY_PUB_USER_FIELD_NUMBER: _ClassVar[int]
    MATRIX_USER_FIELD_NUMBER: _ClassVar[int]
    XMPP_USER_FIELD_NUMBER: _ClassVar[int]
    MATTERMOST_USER_FIELD_NUMBER: _ClassVar[int]
    name: str
    kind: ConnectorKind
    state: ConnectorState
    readiness: ConnectorReadiness
    provisioned_resources: _containers.RepeatedScalarFieldContainer[str]
    webhook_url: str
    tags: _containers.RepeatedScalarFieldContainer[str]
    error_message: str
    create_time: _timestamp_pb2.Timestamp
    update_time: _timestamp_pb2.Timestamp
    display_name: str
    outbox_sms: OutboxSmsConfig
    outbox_rcs: OutboxRcsConfig
    outbox_whatsapp: OutboxWhatsAppConfig
    outbox_email: OutboxEmailConfig
    telegram_bot: TelegramBotConfig
    discord_bot: DiscordBotConfig
    slack_bot: SlackBotConfig
    slack_oauth: SlackOAuthConfig
    teams_bot: TeamsBotConfig
    messenger_bot: MessengerBotConfig
    instagram_bot: InstagramBotConfig
    viber_bot: ViberBotConfig
    line_bot: LineBotConfig
    line_oauth: LineOAuthConfig
    wechat_bot: WeChatBotConfig
    kakao_talk_bot: KakaoTalkBotConfig
    lark_bot: LarkBotConfig
    google_chat_bot: GoogleChatBotConfig
    zoom_chat_s2s: ZoomChatS2SConfig
    webex_bot: WebexBotConfig
    mattermost_bot: MattermostBotConfig
    zendesk: ZendeskConfig
    hubspot: HubspotConfig
    intercom: IntercomConfig
    freshchat: FreshchatConfig
    live_chat: LiveChatConfig
    in_app: InAppConfig
    x_bot: XBotConfig
    linkedin_company: LinkedInCompanyConfig
    reddit_bot: RedditBotConfig
    tiktok_bot: TikTokBotConfig
    twitch_bot: TwitchBotConfig
    bluesky_bot: BlueskyBotConfig
    activity_pub_bot: ActivityPubBotConfig
    apple_messages: AppleMessagesConfig
    whatsapp_bot: WhatsAppBotConfig
    telegram_user: TelegramUserConfig
    x_user: XUserConfig
    linkedin_user: LinkedInUserConfig
    reddit_user: RedditUserConfig
    bluesky_user: BlueskyUserConfig
    tiktok_user: TikTokUserConfig
    twitch_user: TwitchUserConfig
    google_chat_user: GoogleChatUserConfig
    zoom_chat_user: ZoomChatUserConfig
    webex_user: WebexUserConfig
    lark_user: LarkUserConfig
    signal_user: SignalUserConfig
    activity_pub_user: ActivityPubUserConfig
    matrix_user: MatrixUserConfig
    xmpp_user: XmppUserConfig
    mattermost_user: MattermostUserConfig
    def __init__(self, name: _Optional[str] = ..., kind: _Optional[_Union[ConnectorKind, str]] = ..., state: _Optional[_Union[ConnectorState, str]] = ..., readiness: _Optional[_Union[ConnectorReadiness, str]] = ..., provisioned_resources: _Optional[_Iterable[str]] = ..., webhook_url: _Optional[str] = ..., tags: _Optional[_Iterable[str]] = ..., error_message: _Optional[str] = ..., create_time: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., update_time: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., display_name: _Optional[str] = ..., outbox_sms: _Optional[_Union[OutboxSmsConfig, _Mapping]] = ..., outbox_rcs: _Optional[_Union[OutboxRcsConfig, _Mapping]] = ..., outbox_whatsapp: _Optional[_Union[OutboxWhatsAppConfig, _Mapping]] = ..., outbox_email: _Optional[_Union[OutboxEmailConfig, _Mapping]] = ..., telegram_bot: _Optional[_Union[TelegramBotConfig, _Mapping]] = ..., discord_bot: _Optional[_Union[DiscordBotConfig, _Mapping]] = ..., slack_bot: _Optional[_Union[SlackBotConfig, _Mapping]] = ..., slack_oauth: _Optional[_Union[SlackOAuthConfig, _Mapping]] = ..., teams_bot: _Optional[_Union[TeamsBotConfig, _Mapping]] = ..., messenger_bot: _Optional[_Union[MessengerBotConfig, _Mapping]] = ..., instagram_bot: _Optional[_Union[InstagramBotConfig, _Mapping]] = ..., viber_bot: _Optional[_Union[ViberBotConfig, _Mapping]] = ..., line_bot: _Optional[_Union[LineBotConfig, _Mapping]] = ..., line_oauth: _Optional[_Union[LineOAuthConfig, _Mapping]] = ..., wechat_bot: _Optional[_Union[WeChatBotConfig, _Mapping]] = ..., kakao_talk_bot: _Optional[_Union[KakaoTalkBotConfig, _Mapping]] = ..., lark_bot: _Optional[_Union[LarkBotConfig, _Mapping]] = ..., google_chat_bot: _Optional[_Union[GoogleChatBotConfig, _Mapping]] = ..., zoom_chat_s2s: _Optional[_Union[ZoomChatS2SConfig, _Mapping]] = ..., webex_bot: _Optional[_Union[WebexBotConfig, _Mapping]] = ..., mattermost_bot: _Optional[_Union[MattermostBotConfig, _Mapping]] = ..., zendesk: _Optional[_Union[ZendeskConfig, _Mapping]] = ..., hubspot: _Optional[_Union[HubspotConfig, _Mapping]] = ..., intercom: _Optional[_Union[IntercomConfig, _Mapping]] = ..., freshchat: _Optional[_Union[FreshchatConfig, _Mapping]] = ..., live_chat: _Optional[_Union[LiveChatConfig, _Mapping]] = ..., in_app: _Optional[_Union[InAppConfig, _Mapping]] = ..., x_bot: _Optional[_Union[XBotConfig, _Mapping]] = ..., linkedin_company: _Optional[_Union[LinkedInCompanyConfig, _Mapping]] = ..., reddit_bot: _Optional[_Union[RedditBotConfig, _Mapping]] = ..., tiktok_bot: _Optional[_Union[TikTokBotConfig, _Mapping]] = ..., twitch_bot: _Optional[_Union[TwitchBotConfig, _Mapping]] = ..., bluesky_bot: _Optional[_Union[BlueskyBotConfig, _Mapping]] = ..., activity_pub_bot: _Optional[_Union[ActivityPubBotConfig, _Mapping]] = ..., apple_messages: _Optional[_Union[AppleMessagesConfig, _Mapping]] = ..., whatsapp_bot: _Optional[_Union[WhatsAppBotConfig, _Mapping]] = ..., telegram_user: _Optional[_Union[TelegramUserConfig, _Mapping]] = ..., x_user: _Optional[_Union[XUserConfig, _Mapping]] = ..., linkedin_user: _Optional[_Union[LinkedInUserConfig, _Mapping]] = ..., reddit_user: _Optional[_Union[RedditUserConfig, _Mapping]] = ..., bluesky_user: _Optional[_Union[BlueskyUserConfig, _Mapping]] = ..., tiktok_user: _Optional[_Union[TikTokUserConfig, _Mapping]] = ..., twitch_user: _Optional[_Union[TwitchUserConfig, _Mapping]] = ..., google_chat_user: _Optional[_Union[GoogleChatUserConfig, _Mapping]] = ..., zoom_chat_user: _Optional[_Union[ZoomChatUserConfig, _Mapping]] = ..., webex_user: _Optional[_Union[WebexUserConfig, _Mapping]] = ..., lark_user: _Optional[_Union[LarkUserConfig, _Mapping]] = ..., signal_user: _Optional[_Union[SignalUserConfig, _Mapping]] = ..., activity_pub_user: _Optional[_Union[ActivityPubUserConfig, _Mapping]] = ..., matrix_user: _Optional[_Union[MatrixUserConfig, _Mapping]] = ..., xmpp_user: _Optional[_Union[XmppUserConfig, _Mapping]] = ..., mattermost_user: _Optional[_Union[MattermostUserConfig, _Mapping]] = ...) -> None: ...

class CreateConnectorRequest(_message.Message):
    __slots__ = ("connector", "request_id", "consent_acknowledged")
    CONNECTOR_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    CONSENT_ACKNOWLEDGED_FIELD_NUMBER: _ClassVar[int]
    connector: Connector
    request_id: str
    consent_acknowledged: bool
    def __init__(self, connector: _Optional[_Union[Connector, _Mapping]] = ..., request_id: _Optional[str] = ..., consent_acknowledged: _Optional[bool] = ...) -> None: ...

class CreateConnectorResponse(_message.Message):
    __slots__ = ("connector", "authorization_url")
    CONNECTOR_FIELD_NUMBER: _ClassVar[int]
    AUTHORIZATION_URL_FIELD_NUMBER: _ClassVar[int]
    connector: Connector
    authorization_url: str
    def __init__(self, connector: _Optional[_Union[Connector, _Mapping]] = ..., authorization_url: _Optional[str] = ...) -> None: ...

class CreateManagedConnectorRequest(_message.Message):
    __slots__ = ("channel", "filters", "webhook_url", "tags", "request_id")
    class FiltersEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    CHANNEL_FIELD_NUMBER: _ClassVar[int]
    FILTERS_FIELD_NUMBER: _ClassVar[int]
    WEBHOOK_URL_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    channel: str
    filters: _containers.ScalarMap[str, str]
    webhook_url: str
    tags: _containers.RepeatedScalarFieldContainer[str]
    request_id: str
    def __init__(self, channel: _Optional[str] = ..., filters: _Optional[_Mapping[str, str]] = ..., webhook_url: _Optional[str] = ..., tags: _Optional[_Iterable[str]] = ..., request_id: _Optional[str] = ...) -> None: ...

class ProvisionResourceMetadata(_message.Message):
    __slots__ = ("state", "status_message", "progress_percent")
    STATE_FIELD_NUMBER: _ClassVar[int]
    STATUS_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    PROGRESS_PERCENT_FIELD_NUMBER: _ClassVar[int]
    state: ProvisionedResourceState
    status_message: str
    progress_percent: int
    def __init__(self, state: _Optional[_Union[ProvisionedResourceState, str]] = ..., status_message: _Optional[str] = ..., progress_percent: _Optional[int] = ...) -> None: ...

class CreateManagedConnectorMetadata(_message.Message):
    __slots__ = ("current_step", "provision_metadata")
    class Step(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        STEP_UNSPECIFIED: _ClassVar[CreateManagedConnectorMetadata.Step]
        STEP_SEARCHING: _ClassVar[CreateManagedConnectorMetadata.Step]
        STEP_PROVISIONING: _ClassVar[CreateManagedConnectorMetadata.Step]
        STEP_ATTACHING: _ClassVar[CreateManagedConnectorMetadata.Step]
    STEP_UNSPECIFIED: CreateManagedConnectorMetadata.Step
    STEP_SEARCHING: CreateManagedConnectorMetadata.Step
    STEP_PROVISIONING: CreateManagedConnectorMetadata.Step
    STEP_ATTACHING: CreateManagedConnectorMetadata.Step
    CURRENT_STEP_FIELD_NUMBER: _ClassVar[int]
    PROVISION_METADATA_FIELD_NUMBER: _ClassVar[int]
    current_step: CreateManagedConnectorMetadata.Step
    provision_metadata: ProvisionResourceMetadata
    def __init__(self, current_step: _Optional[_Union[CreateManagedConnectorMetadata.Step, str]] = ..., provision_metadata: _Optional[_Union[ProvisionResourceMetadata, _Mapping]] = ...) -> None: ...

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

class VerifyConnectorRequest(_message.Message):
    __slots__ = ("name", "code", "password")
    NAME_FIELD_NUMBER: _ClassVar[int]
    CODE_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    name: str
    code: str
    password: str
    def __init__(self, name: _Optional[str] = ..., code: _Optional[str] = ..., password: _Optional[str] = ...) -> None: ...

class VerifyConnectorResponse(_message.Message):
    __slots__ = ("connector",)
    CONNECTOR_FIELD_NUMBER: _ClassVar[int]
    connector: Connector
    def __init__(self, connector: _Optional[_Union[Connector, _Mapping]] = ...) -> None: ...

class DetachProvisionedResourceRequest(_message.Message):
    __slots__ = ("name",)
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...

class DetachProvisionedResourceResponse(_message.Message):
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
    __slots__ = ("connector", "authorization_url")
    CONNECTOR_FIELD_NUMBER: _ClassVar[int]
    AUTHORIZATION_URL_FIELD_NUMBER: _ClassVar[int]
    connector: Connector
    authorization_url: str
    def __init__(self, connector: _Optional[_Union[Connector, _Mapping]] = ..., authorization_url: _Optional[str] = ...) -> None: ...

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
