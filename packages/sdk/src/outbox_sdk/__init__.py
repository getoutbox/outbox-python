# packages/sdk/src/outbox_sdk/__init__.py
from __future__ import annotations

from typing import TYPE_CHECKING, Self

from connectrpc.interceptor import MetadataInterceptor
from outbox_sdk._delivery import (
    parse,
    verify,
)
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
    ProvisionedResourceState,
    TemplateCategory,
    TemplateStatus,
)
from outbox_sdk._resource_names import parse_id
from outbox_sdk._types import (
    Account,
    ChannelConfigType,
    Connector,
    CreateConnectorResult,
    DeliveryEvent,
    DeliveryUpdateEvent,
    Destination,
    DestinationTargetType,
    DestinationTestResult,
    DestinationTestResultItem,
    Message,
    MessageDelivery,
    MessageEvent,
    MessagePart,
    ReadReceiptDeliveryEvent,
    ReadReceiptEvent,
    ReauthorizeResult,
    Template,
    TypingIndicatorDeliveryEvent,
    TypingIndicatorEvent,
    UnknownDeliveryEvent,
    ValidateFilterResult,
)
from outbox_sdk.namespaces._accounts import AccountsNamespace, ListAccountsResult
from outbox_sdk.namespaces._connectors import ConnectorsNamespace, ListConnectorsResult
from outbox_sdk.namespaces._destinations import DestinationsNamespace, ListDestinationsResult
from outbox_sdk.namespaces._messages import (
    ListMessagesResult,
    MessagesNamespace,
    SendMessageResult,
)
from outbox_sdk.namespaces._templates import ListTemplatesResult, TemplatesNamespace

if TYPE_CHECKING:
    from connectrpc.request import RequestContext

__all__ = [
    "Account",
    "AccountSource",
    "AccountsNamespace",
    "ChannelConfigType",
    "Connector",
    "ConnectorKind",
    "ConnectorReadiness",
    "ConnectorState",
    "ConnectorsNamespace",
    "CreateConnectorResult",
    "DeliveryEvent",
    "DeliveryUpdateEvent",
    "Destination",
    "DestinationEventType",
    "DestinationPayloadFormat",
    "DestinationState",
    "DestinationTargetType",
    "DestinationTestResult",
    "DestinationTestResultItem",
    "DestinationsNamespace",
    "ListAccountsResult",
    "ListConnectorsResult",
    "ListDestinationsResult",
    "ListMessagesResult",
    "ListTemplatesResult",
    "Message",
    "MessageDeletionScope",
    "MessageDelivery",
    "MessageDeliveryStatus",
    "MessageDirection",
    "MessageEvent",
    "MessagePart",
    "MessagePartDisposition",
    "MessagesNamespace",
    "OutboxClient",
    "ProvisionedResourceState",
    "ReadReceiptDeliveryEvent",
    "ReadReceiptEvent",
    "ReauthorizeResult",
    "SendMessageResult",
    "Template",
    "TemplateCategory",
    "TemplateStatus",
    "TemplatesNamespace",
    "TypingIndicatorDeliveryEvent",
    "TypingIndicatorEvent",
    "UnknownDeliveryEvent",
    "ValidateFilterResult",
    "parse",
    "parse_id",
    "verify",
]


class _BearerAuth(MetadataInterceptor[None]):
    """Injects Authorization: Bearer header on every outgoing RPC."""

    def __init__(self, api_key: str) -> None:
        """Initialize with an API key."""
        self._api_key = api_key

    async def on_start(self, ctx: RequestContext[object, object]) -> None:  # type: ignore[override]
        ctx.request_headers()["Authorization"] = f"Bearer {self._api_key}"

    async def on_end(self, token: None, ctx: RequestContext[object, object]) -> None:
        pass


class OutboxClient:
    """Async client for the Outbox messaging API."""

    def __init__(
        self,
        *,
        api_key: str,
        base_url: str = "https://api.outbox.chat",
    ) -> None:
        """Initialize the OutboxClient with an API key and optional base URL."""
        _auth = _BearerAuth(api_key)
        _interceptors = (_auth,)
        self.accounts = AccountsNamespace(base_url, interceptors=_interceptors)
        self.connectors = ConnectorsNamespace(base_url, interceptors=_interceptors)
        self.destinations = DestinationsNamespace(base_url, interceptors=_interceptors)
        self.messages = MessagesNamespace(base_url, interceptors=_interceptors)
        self.templates = TemplatesNamespace(base_url, interceptors=_interceptors)

    async def __aenter__(self) -> Self:
        """Enter async context manager."""
        return self

    async def __aexit__(self, *_: object) -> None:
        """Exit async context manager and close all RPC clients."""
        await self.accounts.close()
        await self.connectors.close()
        await self.destinations.close()
        await self.messages.close()
        await self.templates.close()
