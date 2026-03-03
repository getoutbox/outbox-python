# packages/sdk/src/outbox_sdk/namespaces/_connectors.py
from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from google.protobuf.field_mask_pb2 import FieldMask
from outbox.v1.connector_connect import ConnectorServiceClient
from outbox.v1.connector_pb2 import (
    ActivateConnectorRequest,
    CreateConnectorRequest,
    DeactivateConnectorRequest,
    DeleteConnectorRequest,
    GetConnectorRequest,
    ListConnectorsRequest,
    ReauthorizeConnectorRequest,
    UpdateConnectorRequest,
)
from outbox.v1.connector_pb2 import (
    Connector as ProtoConnector,
)
from outbox_sdk._field_mask import derive_field_mask
from outbox_sdk._mappers import map_connector
from outbox_sdk._resource_names import connector_name
from outbox_sdk._types import ChannelConfigType, CreateConnectorResult

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

    async def close(self) -> None:
        await self._client.close()

    async def create(
        self,
        *,
        channel_config_type: ChannelConfigType,
        channel_config: dict[str, object],
        tags: list[str] | None = None,
        request_id: str = "",
    ) -> CreateConnectorResult:
        if channel_config_type not in _VALID_CHANNEL_CONFIG_TYPES:
            msg = f"Invalid channel_config_type: {channel_config_type!r}"
            raise ValueError(msg)
        connector = ProtoConnector()
        cfg = getattr(connector, channel_config_type)
        for k, v in channel_config.items():
            setattr(cfg, k, v)
        if tags is not None:
            connector.tags.extend(tags)
        req = CreateConnectorRequest(connector=connector, request_id=request_id)
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
    ) -> Connector:
        fields: dict[str, object] = {"tags": tags}
        connector = ProtoConnector(name=connector_name(id_))
        if tags is not None:
            connector.tags.extend(tags)
        if channel_config_type and channel_config:
            if channel_config_type not in _VALID_CHANNEL_CONFIG_TYPES:
                msg = f"Invalid channel_config_type: {channel_config_type!r}"
                raise ValueError(msg)
            cfg = getattr(connector, channel_config_type)
            fields[channel_config_type] = channel_config
            for k, v in channel_config.items():
                setattr(cfg, k, v)
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

    async def reauthorize(self, id_: str) -> str:
        """Trigger a new OAuth flow for an existing connector.

        Returns the authorization URL to redirect the user to.
        Raises an error for static-credential channels.
        """
        req = ReauthorizeConnectorRequest(name=connector_name(id_))
        res = await self._client.reauthorize_connector(req)
        return res.authorization_url
