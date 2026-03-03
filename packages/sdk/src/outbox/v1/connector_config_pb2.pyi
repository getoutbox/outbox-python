from buf.validate import validate_pb2 as _validate_pb2
from google.api import field_behavior_pb2 as _field_behavior_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class ActivityPubConfig(_message.Message):
    __slots__ = ("actor_url", "private_key")
    ACTOR_URL_FIELD_NUMBER: _ClassVar[int]
    PRIVATE_KEY_FIELD_NUMBER: _ClassVar[int]
    actor_url: str
    private_key: str
    def __init__(self, actor_url: _Optional[str] = ..., private_key: _Optional[str] = ...) -> None: ...

class ApnsConfig(_message.Message):
    __slots__ = ("key_id", "team_id", "private_key")
    KEY_ID_FIELD_NUMBER: _ClassVar[int]
    TEAM_ID_FIELD_NUMBER: _ClassVar[int]
    PRIVATE_KEY_FIELD_NUMBER: _ClassVar[int]
    key_id: str
    team_id: str
    private_key: str
    def __init__(self, key_id: _Optional[str] = ..., team_id: _Optional[str] = ..., private_key: _Optional[str] = ...) -> None: ...

class AppleMessagesConfig(_message.Message):
    __slots__ = ("business_id", "msp_id")
    BUSINESS_ID_FIELD_NUMBER: _ClassVar[int]
    MSP_ID_FIELD_NUMBER: _ClassVar[int]
    business_id: str
    msp_id: str
    def __init__(self, business_id: _Optional[str] = ..., msp_id: _Optional[str] = ...) -> None: ...

class BlueskyConfig(_message.Message):
    __slots__ = ("handle", "app_password")
    HANDLE_FIELD_NUMBER: _ClassVar[int]
    APP_PASSWORD_FIELD_NUMBER: _ClassVar[int]
    handle: str
    app_password: str
    def __init__(self, handle: _Optional[str] = ..., app_password: _Optional[str] = ...) -> None: ...

class DiscordConfig(_message.Message):
    __slots__ = ("bot_token",)
    BOT_TOKEN_FIELD_NUMBER: _ClassVar[int]
    bot_token: str
    def __init__(self, bot_token: _Optional[str] = ...) -> None: ...

class EmailConfig(_message.Message):
    __slots__ = ("api_key", "from_address")
    API_KEY_FIELD_NUMBER: _ClassVar[int]
    FROM_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    api_key: str
    from_address: str
    def __init__(self, api_key: _Optional[str] = ..., from_address: _Optional[str] = ...) -> None: ...

class FcmConfig(_message.Message):
    __slots__ = ("service_account_key",)
    SERVICE_ACCOUNT_KEY_FIELD_NUMBER: _ClassVar[int]
    service_account_key: str
    def __init__(self, service_account_key: _Optional[str] = ...) -> None: ...

class FreshchatConfig(_message.Message):
    __slots__ = ("app_id", "api_token")
    APP_ID_FIELD_NUMBER: _ClassVar[int]
    API_TOKEN_FIELD_NUMBER: _ClassVar[int]
    app_id: str
    api_token: str
    def __init__(self, app_id: _Optional[str] = ..., api_token: _Optional[str] = ...) -> None: ...

class InAppConfig(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class MatrixConfig(_message.Message):
    __slots__ = ("homeserver_url", "access_token")
    HOMESERVER_URL_FIELD_NUMBER: _ClassVar[int]
    ACCESS_TOKEN_FIELD_NUMBER: _ClassVar[int]
    homeserver_url: str
    access_token: str
    def __init__(self, homeserver_url: _Optional[str] = ..., access_token: _Optional[str] = ...) -> None: ...

class MqttConfig(_message.Message):
    __slots__ = ("broker_url", "username", "password")
    BROKER_URL_FIELD_NUMBER: _ClassVar[int]
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    broker_url: str
    username: str
    password: str
    def __init__(self, broker_url: _Optional[str] = ..., username: _Optional[str] = ..., password: _Optional[str] = ...) -> None: ...

class RcsConfig(_message.Message):
    __slots__ = ("service_account_key",)
    SERVICE_ACCOUNT_KEY_FIELD_NUMBER: _ClassVar[int]
    service_account_key: str
    def __init__(self, service_account_key: _Optional[str] = ...) -> None: ...

class SignalConfig(_message.Message):
    __slots__ = ("url", "phone_number")
    URL_FIELD_NUMBER: _ClassVar[int]
    PHONE_NUMBER_FIELD_NUMBER: _ClassVar[int]
    url: str
    phone_number: str
    def __init__(self, url: _Optional[str] = ..., phone_number: _Optional[str] = ...) -> None: ...

class SmsConfig(_message.Message):
    __slots__ = ("account_sid", "auth_token", "from_number")
    ACCOUNT_SID_FIELD_NUMBER: _ClassVar[int]
    AUTH_TOKEN_FIELD_NUMBER: _ClassVar[int]
    FROM_NUMBER_FIELD_NUMBER: _ClassVar[int]
    account_sid: str
    auth_token: str
    from_number: str
    def __init__(self, account_sid: _Optional[str] = ..., auth_token: _Optional[str] = ..., from_number: _Optional[str] = ...) -> None: ...

class TelegramConfig(_message.Message):
    __slots__ = ("bot_token",)
    BOT_TOKEN_FIELD_NUMBER: _ClassVar[int]
    bot_token: str
    def __init__(self, bot_token: _Optional[str] = ...) -> None: ...

class ViberConfig(_message.Message):
    __slots__ = ("auth_token",)
    AUTH_TOKEN_FIELD_NUMBER: _ClassVar[int]
    auth_token: str
    def __init__(self, auth_token: _Optional[str] = ...) -> None: ...

class WebPushConfig(_message.Message):
    __slots__ = ("vapid_public_key", "vapid_private_key")
    VAPID_PUBLIC_KEY_FIELD_NUMBER: _ClassVar[int]
    VAPID_PRIVATE_KEY_FIELD_NUMBER: _ClassVar[int]
    vapid_public_key: str
    vapid_private_key: str
    def __init__(self, vapid_public_key: _Optional[str] = ..., vapid_private_key: _Optional[str] = ...) -> None: ...

class XmppConfig(_message.Message):
    __slots__ = ("server", "username", "password")
    SERVER_FIELD_NUMBER: _ClassVar[int]
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    server: str
    username: str
    password: str
    def __init__(self, server: _Optional[str] = ..., username: _Optional[str] = ..., password: _Optional[str] = ...) -> None: ...

class TeamsConfig(_message.Message):
    __slots__ = ("tenant_id", "client_id", "client_secret")
    TENANT_ID_FIELD_NUMBER: _ClassVar[int]
    CLIENT_ID_FIELD_NUMBER: _ClassVar[int]
    CLIENT_SECRET_FIELD_NUMBER: _ClassVar[int]
    tenant_id: str
    client_id: str
    client_secret: str
    def __init__(self, tenant_id: _Optional[str] = ..., client_id: _Optional[str] = ..., client_secret: _Optional[str] = ...) -> None: ...

class WechatConfig(_message.Message):
    __slots__ = ("app_id", "app_secret", "token")
    APP_ID_FIELD_NUMBER: _ClassVar[int]
    APP_SECRET_FIELD_NUMBER: _ClassVar[int]
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    app_id: str
    app_secret: str
    token: str
    def __init__(self, app_id: _Optional[str] = ..., app_secret: _Optional[str] = ..., token: _Optional[str] = ...) -> None: ...

class HubspotConfig(_message.Message):
    __slots__ = ("client_id", "client_secret", "portal_id")
    CLIENT_ID_FIELD_NUMBER: _ClassVar[int]
    CLIENT_SECRET_FIELD_NUMBER: _ClassVar[int]
    PORTAL_ID_FIELD_NUMBER: _ClassVar[int]
    client_id: str
    client_secret: str
    portal_id: str
    def __init__(self, client_id: _Optional[str] = ..., client_secret: _Optional[str] = ..., portal_id: _Optional[str] = ...) -> None: ...

class IntercomConfig(_message.Message):
    __slots__ = ("app_id", "app_secret", "workspace_name")
    APP_ID_FIELD_NUMBER: _ClassVar[int]
    APP_SECRET_FIELD_NUMBER: _ClassVar[int]
    WORKSPACE_NAME_FIELD_NUMBER: _ClassVar[int]
    app_id: str
    app_secret: str
    workspace_name: str
    def __init__(self, app_id: _Optional[str] = ..., app_secret: _Optional[str] = ..., workspace_name: _Optional[str] = ...) -> None: ...

class LinkedinConfig(_message.Message):
    __slots__ = ("client_id", "client_secret", "profile_name")
    CLIENT_ID_FIELD_NUMBER: _ClassVar[int]
    CLIENT_SECRET_FIELD_NUMBER: _ClassVar[int]
    PROFILE_NAME_FIELD_NUMBER: _ClassVar[int]
    client_id: str
    client_secret: str
    profile_name: str
    def __init__(self, client_id: _Optional[str] = ..., client_secret: _Optional[str] = ..., profile_name: _Optional[str] = ...) -> None: ...

class LiveChatConfig(_message.Message):
    __slots__ = ("client_id", "client_secret")
    CLIENT_ID_FIELD_NUMBER: _ClassVar[int]
    CLIENT_SECRET_FIELD_NUMBER: _ClassVar[int]
    client_id: str
    client_secret: str
    def __init__(self, client_id: _Optional[str] = ..., client_secret: _Optional[str] = ...) -> None: ...

class RedditConfig(_message.Message):
    __slots__ = ("client_id", "client_secret", "username")
    CLIENT_ID_FIELD_NUMBER: _ClassVar[int]
    CLIENT_SECRET_FIELD_NUMBER: _ClassVar[int]
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    client_id: str
    client_secret: str
    username: str
    def __init__(self, client_id: _Optional[str] = ..., client_secret: _Optional[str] = ..., username: _Optional[str] = ...) -> None: ...

class ThreadsConfig(_message.Message):
    __slots__ = ("app_id", "app_secret", "user_id")
    APP_ID_FIELD_NUMBER: _ClassVar[int]
    APP_SECRET_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    app_id: str
    app_secret: str
    user_id: str
    def __init__(self, app_id: _Optional[str] = ..., app_secret: _Optional[str] = ..., user_id: _Optional[str] = ...) -> None: ...

class TiktokConfig(_message.Message):
    __slots__ = ("client_key", "client_secret", "open_id")
    CLIENT_KEY_FIELD_NUMBER: _ClassVar[int]
    CLIENT_SECRET_FIELD_NUMBER: _ClassVar[int]
    OPEN_ID_FIELD_NUMBER: _ClassVar[int]
    client_key: str
    client_secret: str
    open_id: str
    def __init__(self, client_key: _Optional[str] = ..., client_secret: _Optional[str] = ..., open_id: _Optional[str] = ...) -> None: ...

class TwitchConfig(_message.Message):
    __slots__ = ("client_id", "client_secret", "bot_username")
    CLIENT_ID_FIELD_NUMBER: _ClassVar[int]
    CLIENT_SECRET_FIELD_NUMBER: _ClassVar[int]
    BOT_USERNAME_FIELD_NUMBER: _ClassVar[int]
    client_id: str
    client_secret: str
    bot_username: str
    def __init__(self, client_id: _Optional[str] = ..., client_secret: _Optional[str] = ..., bot_username: _Optional[str] = ...) -> None: ...

class ZaloConfig(_message.Message):
    __slots__ = ("app_id", "app_secret", "oa_id")
    APP_ID_FIELD_NUMBER: _ClassVar[int]
    APP_SECRET_FIELD_NUMBER: _ClassVar[int]
    OA_ID_FIELD_NUMBER: _ClassVar[int]
    app_id: str
    app_secret: str
    oa_id: str
    def __init__(self, app_id: _Optional[str] = ..., app_secret: _Optional[str] = ..., oa_id: _Optional[str] = ...) -> None: ...

class ZendeskConfig(_message.Message):
    __slots__ = ("subdomain", "client_id", "client_secret", "account_name")
    SUBDOMAIN_FIELD_NUMBER: _ClassVar[int]
    CLIENT_ID_FIELD_NUMBER: _ClassVar[int]
    CLIENT_SECRET_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_NAME_FIELD_NUMBER: _ClassVar[int]
    subdomain: str
    client_id: str
    client_secret: str
    account_name: str
    def __init__(self, subdomain: _Optional[str] = ..., client_id: _Optional[str] = ..., client_secret: _Optional[str] = ..., account_name: _Optional[str] = ...) -> None: ...

class InstagramConfig(_message.Message):
    __slots__ = ("app_id", "app_secret", "page_id", "instagram_account_id")
    APP_ID_FIELD_NUMBER: _ClassVar[int]
    APP_SECRET_FIELD_NUMBER: _ClassVar[int]
    PAGE_ID_FIELD_NUMBER: _ClassVar[int]
    INSTAGRAM_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    app_id: str
    app_secret: str
    page_id: str
    instagram_account_id: str
    def __init__(self, app_id: _Optional[str] = ..., app_secret: _Optional[str] = ..., page_id: _Optional[str] = ..., instagram_account_id: _Optional[str] = ...) -> None: ...

class MessengerConfig(_message.Message):
    __slots__ = ("app_id", "app_secret", "page_id", "page_name")
    APP_ID_FIELD_NUMBER: _ClassVar[int]
    APP_SECRET_FIELD_NUMBER: _ClassVar[int]
    PAGE_ID_FIELD_NUMBER: _ClassVar[int]
    PAGE_NAME_FIELD_NUMBER: _ClassVar[int]
    app_id: str
    app_secret: str
    page_id: str
    page_name: str
    def __init__(self, app_id: _Optional[str] = ..., app_secret: _Optional[str] = ..., page_id: _Optional[str] = ..., page_name: _Optional[str] = ...) -> None: ...

class WhatsAppConfig(_message.Message):
    __slots__ = ("app_id", "app_secret", "waba_id", "phone_number_id", "display_phone_number")
    APP_ID_FIELD_NUMBER: _ClassVar[int]
    APP_SECRET_FIELD_NUMBER: _ClassVar[int]
    WABA_ID_FIELD_NUMBER: _ClassVar[int]
    PHONE_NUMBER_ID_FIELD_NUMBER: _ClassVar[int]
    DISPLAY_PHONE_NUMBER_FIELD_NUMBER: _ClassVar[int]
    app_id: str
    app_secret: str
    waba_id: str
    phone_number_id: str
    display_phone_number: str
    def __init__(self, app_id: _Optional[str] = ..., app_secret: _Optional[str] = ..., waba_id: _Optional[str] = ..., phone_number_id: _Optional[str] = ..., display_phone_number: _Optional[str] = ...) -> None: ...

class GoogleChatConfig(_message.Message):
    __slots__ = ("service_account_key", "client_id", "client_secret", "space_id")
    SERVICE_ACCOUNT_KEY_FIELD_NUMBER: _ClassVar[int]
    CLIENT_ID_FIELD_NUMBER: _ClassVar[int]
    CLIENT_SECRET_FIELD_NUMBER: _ClassVar[int]
    SPACE_ID_FIELD_NUMBER: _ClassVar[int]
    service_account_key: str
    client_id: str
    client_secret: str
    space_id: str
    def __init__(self, service_account_key: _Optional[str] = ..., client_id: _Optional[str] = ..., client_secret: _Optional[str] = ..., space_id: _Optional[str] = ...) -> None: ...

class KakaoTalkConfig(_message.Message):
    __slots__ = ("biz_client_id", "biz_client_secret", "rest_api_key", "client_secret", "kakao_user_id", "channel_name")
    BIZ_CLIENT_ID_FIELD_NUMBER: _ClassVar[int]
    BIZ_CLIENT_SECRET_FIELD_NUMBER: _ClassVar[int]
    REST_API_KEY_FIELD_NUMBER: _ClassVar[int]
    CLIENT_SECRET_FIELD_NUMBER: _ClassVar[int]
    KAKAO_USER_ID_FIELD_NUMBER: _ClassVar[int]
    CHANNEL_NAME_FIELD_NUMBER: _ClassVar[int]
    biz_client_id: str
    biz_client_secret: str
    rest_api_key: str
    client_secret: str
    kakao_user_id: str
    channel_name: str
    def __init__(self, biz_client_id: _Optional[str] = ..., biz_client_secret: _Optional[str] = ..., rest_api_key: _Optional[str] = ..., client_secret: _Optional[str] = ..., kakao_user_id: _Optional[str] = ..., channel_name: _Optional[str] = ...) -> None: ...

class LarkConfig(_message.Message):
    __slots__ = ("app_id", "app_secret", "user_oauth", "tenant_name")
    APP_ID_FIELD_NUMBER: _ClassVar[int]
    APP_SECRET_FIELD_NUMBER: _ClassVar[int]
    USER_OAUTH_FIELD_NUMBER: _ClassVar[int]
    TENANT_NAME_FIELD_NUMBER: _ClassVar[int]
    app_id: str
    app_secret: str
    user_oauth: bool
    tenant_name: str
    def __init__(self, app_id: _Optional[str] = ..., app_secret: _Optional[str] = ..., user_oauth: _Optional[bool] = ..., tenant_name: _Optional[str] = ...) -> None: ...

class LineConfig(_message.Message):
    __slots__ = ("channel_token", "channel_secret", "channel_id", "bot_name")
    CHANNEL_TOKEN_FIELD_NUMBER: _ClassVar[int]
    CHANNEL_SECRET_FIELD_NUMBER: _ClassVar[int]
    CHANNEL_ID_FIELD_NUMBER: _ClassVar[int]
    BOT_NAME_FIELD_NUMBER: _ClassVar[int]
    channel_token: str
    channel_secret: str
    channel_id: str
    bot_name: str
    def __init__(self, channel_token: _Optional[str] = ..., channel_secret: _Optional[str] = ..., channel_id: _Optional[str] = ..., bot_name: _Optional[str] = ...) -> None: ...

class MattermostConfig(_message.Message):
    __slots__ = ("url", "bot_token", "admin_token", "bot_username")
    URL_FIELD_NUMBER: _ClassVar[int]
    BOT_TOKEN_FIELD_NUMBER: _ClassVar[int]
    ADMIN_TOKEN_FIELD_NUMBER: _ClassVar[int]
    BOT_USERNAME_FIELD_NUMBER: _ClassVar[int]
    url: str
    bot_token: str
    admin_token: str
    bot_username: str
    def __init__(self, url: _Optional[str] = ..., bot_token: _Optional[str] = ..., admin_token: _Optional[str] = ..., bot_username: _Optional[str] = ...) -> None: ...

class SlackConfig(_message.Message):
    __slots__ = ("bot_token", "signing_secret", "client_id", "client_secret", "team_name", "bot_user_id")
    BOT_TOKEN_FIELD_NUMBER: _ClassVar[int]
    SIGNING_SECRET_FIELD_NUMBER: _ClassVar[int]
    CLIENT_ID_FIELD_NUMBER: _ClassVar[int]
    CLIENT_SECRET_FIELD_NUMBER: _ClassVar[int]
    TEAM_NAME_FIELD_NUMBER: _ClassVar[int]
    BOT_USER_ID_FIELD_NUMBER: _ClassVar[int]
    bot_token: str
    signing_secret: str
    client_id: str
    client_secret: str
    team_name: str
    bot_user_id: str
    def __init__(self, bot_token: _Optional[str] = ..., signing_secret: _Optional[str] = ..., client_id: _Optional[str] = ..., client_secret: _Optional[str] = ..., team_name: _Optional[str] = ..., bot_user_id: _Optional[str] = ...) -> None: ...

class WebexConfig(_message.Message):
    __slots__ = ("bot_token", "client_id", "client_secret", "display_name")
    BOT_TOKEN_FIELD_NUMBER: _ClassVar[int]
    CLIENT_ID_FIELD_NUMBER: _ClassVar[int]
    CLIENT_SECRET_FIELD_NUMBER: _ClassVar[int]
    DISPLAY_NAME_FIELD_NUMBER: _ClassVar[int]
    bot_token: str
    client_id: str
    client_secret: str
    display_name: str
    def __init__(self, bot_token: _Optional[str] = ..., client_id: _Optional[str] = ..., client_secret: _Optional[str] = ..., display_name: _Optional[str] = ...) -> None: ...

class XConfig(_message.Message):
    __slots__ = ("client_id", "client_secret", "bearer_token", "username")
    CLIENT_ID_FIELD_NUMBER: _ClassVar[int]
    CLIENT_SECRET_FIELD_NUMBER: _ClassVar[int]
    BEARER_TOKEN_FIELD_NUMBER: _ClassVar[int]
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    client_id: str
    client_secret: str
    bearer_token: str
    username: str
    def __init__(self, client_id: _Optional[str] = ..., client_secret: _Optional[str] = ..., bearer_token: _Optional[str] = ..., username: _Optional[str] = ...) -> None: ...

class ZoomChatConfig(_message.Message):
    __slots__ = ("client_id", "client_secret", "account_id", "user_email")
    CLIENT_ID_FIELD_NUMBER: _ClassVar[int]
    CLIENT_SECRET_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    USER_EMAIL_FIELD_NUMBER: _ClassVar[int]
    client_id: str
    client_secret: str
    account_id: str
    user_email: str
    def __init__(self, client_id: _Optional[str] = ..., client_secret: _Optional[str] = ..., account_id: _Optional[str] = ..., user_email: _Optional[str] = ...) -> None: ...
