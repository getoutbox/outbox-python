# packages/sdk/src/outbox_sdk/namespaces/_connectors.py
from __future__ import annotations

import asyncio
from dataclasses import dataclass
from typing import TYPE_CHECKING

from google.longrunning.operations_connect import OperationsClient  # type: ignore[reportMissingTypeStubs]
from google.longrunning.operations_pb2 import GetOperationRequest
from google.protobuf.field_mask_pb2 import FieldMask
from outbox.v1.connector_connect import ConnectorServiceClient
from outbox.v1.connector_pb2 import (
    ActivateConnectorRequest,
    CreateConnectorRequest,
    CreateManagedConnectorRequest,
    DeactivateConnectorRequest,
    DeleteConnectorRequest,
    DetachProvisionedResourceRequest,
    GetConnectorRequest,
    ListConnectorsRequest,
    ReauthorizeConnectorRequest,
    UpdateConnectorRequest,
    VerifyConnectorRequest,
)
from outbox.v1.connector_pb2 import (
    Connector as ProtoConnector,
)
from outbox_sdk._field_mask import derive_field_mask
from outbox_sdk._mappers import map_connector
from outbox_sdk._resource_names import connector_name
from outbox_sdk._types import ChannelConfigType, CreateConnectorResult, ReauthorizeResult

if TYPE_CHECKING:
    from connectrpc.interceptor import Interceptor
    from outbox_sdk._types import Connector

_VALID_CHANNEL_CONFIG_TYPES: frozenset[str] = frozenset(
    ChannelConfigType.__args__  # type: ignore[attr-defined]
)


@dataclass
class ListConnectorsResult:
    items: list[Connector]
    next_page_token: str | None
    total_size: int


class ConnectorsNamespace:
    def __init__(self, base_url: str, interceptors: tuple[Interceptor, ...] = ()) -> None:  # type: ignore[reportUnknownParameterType]
        self._client = ConnectorServiceClient(base_url, interceptors=interceptors)
        self._ops_client = OperationsClient(base_url, interceptors=interceptors)
        # _poll_interval controls seconds between LRO polls. Zero skips the sleep (used in tests).
        self._poll_interval: float = 2.0

    async def close(self) -> None:
        await self._client.close()
        await self._ops_client.close()

    async def create(
        self,
        *,
        channel_config_type: ChannelConfigType,
        channel_config: dict[str, object],
        tags: list[str] | None = None,
        request_id: str = "",
        consent_acknowledged: bool = False,
    ) -> CreateConnectorResult:
        if channel_config_type not in _VALID_CHANNEL_CONFIG_TYPES:
            msg = f"Invalid channel_config_type: {channel_config_type!r}"
            raise ValueError(msg)
        connector = ProtoConnector()
        cfg = getattr(connector, channel_config_type)
        for k, v in channel_config.items():
            setattr(cfg, k, v)
        cfg.SetInParent()  # ensures oneof is set even for zero-field configs
        if tags is not None:
            connector.tags.extend(tags)
        req = CreateConnectorRequest(
            connector=connector,
            request_id=request_id,
            consent_acknowledged=consent_acknowledged,
        )
        res = await self._client.create_connector(req)
        if not res.HasField("connector"):
            msg = "create_connector: server returned empty connector"
            raise RuntimeError(msg)
        return CreateConnectorResult(
            connector=map_connector(res.connector),
            authorization_url=res.authorization_url or None,
        )

    async def get(self, id_: str) -> Connector:
        req = GetConnectorRequest(name=connector_name(id_))
        res = await self._client.get_connector(req)
        if not res.HasField("connector"):
            msg = "get_connector: server returned empty connector"
            raise RuntimeError(msg)
        return map_connector(res.connector)

    async def list(
        self,
        *,
        filter_: str = "",
        order_by: str = "",
        page_size: int = 0,
        page_token: str = "",
    ) -> ListConnectorsResult:
        req = ListConnectorsRequest(
            filter=filter_,
            order_by=order_by,
            page_size=page_size,
            page_token=page_token,
        )
        res = await self._client.list_connectors(req)
        return ListConnectorsResult(
            items=[map_connector(c) for c in res.connectors],
            next_page_token=res.next_page_token or None,
            total_size=res.total_size,
        )

    async def update(
        self,
        *,
        id_: str,
        channel_config_type: ChannelConfigType | None = None,
        channel_config: dict[str, object] | None = None,
        tags: list[str] | None = None,
        webhook_url: str | None = None,
    ) -> Connector:
        fields: dict[str, object] = {"tags": tags, "webhook_url": webhook_url}
        connector = ProtoConnector(name=connector_name(id_))
        if tags is not None:
            connector.tags.extend(tags)
        if webhook_url is not None:
            connector.webhook_url = webhook_url
        if channel_config_type is not None:
            if channel_config_type not in _VALID_CHANNEL_CONFIG_TYPES:
                msg = f"Invalid channel_config_type: {channel_config_type!r}"
                raise ValueError(msg)
            cfg = getattr(connector, channel_config_type)
            fields[channel_config_type] = channel_config or {}
            for k, v in (channel_config or {}).items():
                setattr(cfg, k, v)
            cfg.SetInParent()  # ensures oneof is set even for zero-field configs
        req = UpdateConnectorRequest(
            connector=connector,
            update_mask=FieldMask(paths=derive_field_mask(fields)),
        )
        res = await self._client.update_connector(req)
        if not res.HasField("connector"):
            msg = "update_connector: server returned empty connector"
            raise RuntimeError(msg)
        return map_connector(res.connector)

    async def delete(self, id_: str) -> None:
        req = DeleteConnectorRequest(name=connector_name(id_))
        await self._client.delete_connector(req)

    async def activate(self, id_: str) -> Connector:
        req = ActivateConnectorRequest(name=connector_name(id_))
        res = await self._client.activate_connector(req)
        if not res.HasField("connector"):
            msg = "activate_connector: server returned empty connector"
            raise RuntimeError(msg)
        return map_connector(res.connector)

    async def deactivate(self, id_: str) -> Connector:
        req = DeactivateConnectorRequest(name=connector_name(id_))
        res = await self._client.deactivate_connector(req)
        if not res.HasField("connector"):
            msg = "deactivate_connector: server returned empty connector"
            raise RuntimeError(msg)
        return map_connector(res.connector)

    async def reauthorize(self, id_: str) -> ReauthorizeResult:
        """Trigger a new OAuth flow for an existing connector."""
        req = ReauthorizeConnectorRequest(name=connector_name(id_))
        res = await self._client.reauthorize_connector(req)
        if not res.HasField("connector"):
            msg = "reauthorize_connector: server returned empty connector"
            raise RuntimeError(msg)
        return ReauthorizeResult(
            connector=map_connector(res.connector),
            authorization_url=res.authorization_url or None,
        )

    async def verify(self, id_: str, code: str, *, password: str = "") -> Connector:
        """Submit a verification code for a connector (e.g. Telegram/Signal)."""
        req = VerifyConnectorRequest(name=connector_name(id_), code=code, password=password)
        res = await self._client.verify_connector(req)
        if not res.HasField("connector"):
            msg = "verify_connector: server returned empty connector"
            raise RuntimeError(msg)
        return map_connector(res.connector)

    async def detach(self, id_: str) -> Connector:
        """Detach the provisioned resource from a managed connector."""
        req = DetachProvisionedResourceRequest(name=connector_name(id_))
        res = await self._client.detach_provisioned_resource(req)
        if not res.HasField("connector"):
            msg = "detach_provisioned_resource: server returned empty connector"
            raise RuntimeError(msg)
        return map_connector(res.connector)

    async def create_managed(
        self,
        channel: str,
        *,
        filters: dict[str, str] | None = None,
        webhook_url: str = "",
        tags: list[str] | None = None,
        request_id: str = "",
    ) -> Connector:
        """Provision a managed connector for the given channel (LRO)."""
        req = CreateManagedConnectorRequest(
            channel=channel,
            filters=filters or {},
            webhook_url=webhook_url,
            tags=tags or [],
            request_id=request_id,
        )
        op = await self._client.create_managed_connector(req)
        while not op.done:
            if self._poll_interval > 0:
                await asyncio.sleep(self._poll_interval)
            op = await self._ops_client.get_operation(GetOperationRequest(name=op.name))
        if op.HasField("error"):
            err = op.error
            msg = f"create_managed_connector failed: {err.message} (code {err.code})"
            raise RuntimeError(msg)
        connector_proto = ProtoConnector()
        if not op.response.Unpack(connector_proto):  # type: ignore[reportUnknownMemberType]
            msg = "create_managed_connector: failed to unpack response"
            raise RuntimeError(msg)
        return map_connector(connector_proto)
