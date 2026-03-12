"""Tests for ConnectorsNamespace using mocked gRPC clients."""
from __future__ import annotations

from unittest.mock import AsyncMock, patch

import pytest
from google.longrunning.operations_pb2 import Operation
from google.protobuf.any_pb2 import Any as AnyProto
from outbox.v1 import connector_pb2
from outbox_sdk._enums import ConnectorKind, ConnectorReadiness, ConnectorState
from outbox_sdk._types import CreateConnectorResult, ReauthorizeResult
from outbox_sdk.namespaces._connectors import ConnectorsNamespace, ListConnectorsResult


def _make_connector(
    name: str = "connectors/conn-1",
    state: int = connector_pb2.ConnectorState.Value("CONNECTOR_STATE_ACTIVE"),
    kind: int = connector_pb2.ConnectorKind.Value("CONNECTOR_KIND_USER"),
    readiness: int = connector_pb2.ConnectorReadiness.Value("CONNECTOR_READINESS_READY"),
) -> connector_pb2.Connector:
    c = connector_pb2.Connector()
    c.name = name
    c.state = state
    c.kind = kind
    c.readiness = readiness
    c.display_name = "Test Connector"
    c.webhook_url = "https://example.com/webhook"
    return c


@pytest.fixture
def mock_conn_client() -> AsyncMock:
    return AsyncMock()


@pytest.fixture
def mock_ops_client() -> AsyncMock:
    return AsyncMock()


@pytest.fixture
def ns(mock_conn_client: AsyncMock, mock_ops_client: AsyncMock) -> ConnectorsNamespace:
    with (
        patch("outbox_sdk.namespaces._connectors.ConnectorServiceClient") as MockClient,
        patch("outbox_sdk.namespaces._connectors.OperationsClient") as MockOpsClient,
    ):
        MockClient.return_value = mock_conn_client
        MockOpsClient.return_value = mock_ops_client
        instance = ConnectorsNamespace("http://localhost:8080")
        instance._poll_interval = 0  # skip sleeping in tests
        return instance


@pytest.mark.asyncio
async def test_create_success(ns: ConnectorsNamespace, mock_conn_client: AsyncMock) -> None:
    resp = connector_pb2.CreateConnectorResponse()
    resp.connector.CopyFrom(_make_connector())
    mock_conn_client.create_connector = AsyncMock(return_value=resp)

    result = await ns.create(
        channel_config_type="whatsapp_bot",
        channel_config={"app_id": "app123", "app_secret": "secret456"},
    )

    assert isinstance(result, CreateConnectorResult)
    assert result.connector.id == "conn-1"
    assert result.connector.state == ConnectorState.ACTIVE
    assert result.connector.kind == ConnectorKind.USER
    assert result.connector.readiness == ConnectorReadiness.READY
    assert result.connector.display_name == "Test Connector"
    assert result.connector.webhook_url == "https://example.com/webhook"
    assert result.authorization_url is None


@pytest.mark.asyncio
async def test_create_with_authorization_url(ns: ConnectorsNamespace, mock_conn_client: AsyncMock) -> None:
    resp = connector_pb2.CreateConnectorResponse()
    resp.connector.CopyFrom(_make_connector(state=connector_pb2.ConnectorState.Value("CONNECTOR_STATE_AUTHORIZING")))
    resp.authorization_url = "https://oauth.example.com/auth?code=xyz"
    mock_conn_client.create_connector = AsyncMock(return_value=resp)

    result = await ns.create(
        channel_config_type="whatsapp_bot",
        channel_config={"app_id": "app123", "app_secret": "secret456"},
    )

    assert result.connector.state == ConnectorState.AUTHORIZING
    assert result.authorization_url == "https://oauth.example.com/auth?code=xyz"


@pytest.mark.asyncio
async def test_create_builds_correct_proto(ns: ConnectorsNamespace, mock_conn_client: AsyncMock) -> None:
    resp = connector_pb2.CreateConnectorResponse()
    resp.connector.CopyFrom(_make_connector())
    mock_conn_client.create_connector = AsyncMock(return_value=resp)

    await ns.create(
        channel_config_type="whatsapp_bot",
        channel_config={"app_id": "app123", "app_secret": "secret456"},
        tags=["prod", "whatsapp"],
    )

    req = mock_conn_client.create_connector.call_args[0][0]
    assert req.connector.whatsapp_bot.app_id == "app123"
    assert req.connector.whatsapp_bot.app_secret == "secret456"
    assert list(req.connector.tags) == ["prod", "whatsapp"]


@pytest.mark.asyncio
async def test_create_with_consent_acknowledged(ns: ConnectorsNamespace, mock_conn_client: AsyncMock) -> None:
    resp = connector_pb2.CreateConnectorResponse()
    resp.connector.CopyFrom(_make_connector())
    mock_conn_client.create_connector = AsyncMock(return_value=resp)

    await ns.create(
        channel_config_type="whatsapp_bot",
        channel_config={"app_id": "app123"},
        consent_acknowledged=True,
    )

    req = mock_conn_client.create_connector.call_args[0][0]
    assert req.consent_acknowledged is True


@pytest.mark.asyncio
async def test_create_empty_response_raises(ns: ConnectorsNamespace, mock_conn_client: AsyncMock) -> None:
    resp = connector_pb2.CreateConnectorResponse()
    mock_conn_client.create_connector = AsyncMock(return_value=resp)

    with pytest.raises(RuntimeError, match="server returned empty connector"):
        await ns.create(channel_config_type="whatsapp_bot", channel_config={"app_id": "x"})


@pytest.mark.asyncio
async def test_get_success(ns: ConnectorsNamespace, mock_conn_client: AsyncMock) -> None:
    resp = connector_pb2.GetConnectorResponse()
    resp.connector.CopyFrom(_make_connector())
    mock_conn_client.get_connector = AsyncMock(return_value=resp)

    result = await ns.get("conn-1")

    assert result.id == "conn-1"
    assert result.kind == ConnectorKind.USER
    assert result.readiness == ConnectorReadiness.READY
    assert result.display_name == "Test Connector"
    assert result.webhook_url == "https://example.com/webhook"
    req = mock_conn_client.get_connector.call_args[0][0]
    assert req.name == "connectors/conn-1"


@pytest.mark.asyncio
async def test_get_empty_response_raises(ns: ConnectorsNamespace, mock_conn_client: AsyncMock) -> None:
    resp = connector_pb2.GetConnectorResponse()
    mock_conn_client.get_connector = AsyncMock(return_value=resp)

    with pytest.raises(RuntimeError, match="server returned empty connector"):
        await ns.get("conn-1")


@pytest.mark.asyncio
async def test_list_pagination(ns: ConnectorsNamespace, mock_conn_client: AsyncMock) -> None:
    resp = connector_pb2.ListConnectorsResponse()
    resp.connectors.append(_make_connector("connectors/conn-1"))
    resp.connectors.append(_make_connector("connectors/conn-2"))
    resp.next_page_token = "tok-xyz"
    resp.total_size = 5
    mock_conn_client.list_connectors = AsyncMock(return_value=resp)

    result = await ns.list(page_size=2)

    assert isinstance(result, ListConnectorsResult)
    assert len(result.items) == 2
    assert result.items[0].id == "conn-1"
    assert result.next_page_token == "tok-xyz"
    assert result.total_size == 5


@pytest.mark.asyncio
async def test_list_empty_next_page_token(ns: ConnectorsNamespace, mock_conn_client: AsyncMock) -> None:
    resp = connector_pb2.ListConnectorsResponse()
    resp.next_page_token = ""
    mock_conn_client.list_connectors = AsyncMock(return_value=resp)

    result = await ns.list()

    assert result.next_page_token is None


@pytest.mark.asyncio
async def test_update_tags(ns: ConnectorsNamespace, mock_conn_client: AsyncMock) -> None:
    resp = connector_pb2.UpdateConnectorResponse()
    updated = _make_connector()
    updated.tags.extend(["new-tag"])
    resp.connector.CopyFrom(updated)
    mock_conn_client.update_connector = AsyncMock(return_value=resp)

    result = await ns.update(id_="conn-1", tags=["new-tag"])

    assert result.id == "conn-1"
    req = mock_conn_client.update_connector.call_args[0][0]
    assert list(req.connector.tags) == ["new-tag"]
    assert "tags" in list(req.update_mask.paths)


@pytest.mark.asyncio
async def test_update_connector_tags_empty_list(ns: ConnectorsNamespace, mock_conn_client: AsyncMock) -> None:
    resp = connector_pb2.UpdateConnectorResponse()
    resp.connector.CopyFrom(_make_connector())
    mock_conn_client.update_connector = AsyncMock(return_value=resp)

    await ns.update(id_="conn-1", tags=[])

    req = mock_conn_client.update_connector.call_args[0][0]
    assert "tags" in list(req.update_mask.paths)


@pytest.mark.asyncio
async def test_update_channel_config(ns: ConnectorsNamespace, mock_conn_client: AsyncMock) -> None:
    resp = connector_pb2.UpdateConnectorResponse()
    resp.connector.CopyFrom(_make_connector())
    mock_conn_client.update_connector = AsyncMock(return_value=resp)

    await ns.update(
        id_="conn-1",
        channel_config_type="whatsapp_bot",
        channel_config={"app_id": "new-app"},
    )

    req = mock_conn_client.update_connector.call_args[0][0]
    assert req.connector.whatsapp_bot.app_id == "new-app"
    assert "whatsapp_bot" in list(req.update_mask.paths)


@pytest.mark.asyncio
async def test_update_empty_response_raises(ns: ConnectorsNamespace, mock_conn_client: AsyncMock) -> None:
    resp = connector_pb2.UpdateConnectorResponse()
    mock_conn_client.update_connector = AsyncMock(return_value=resp)

    with pytest.raises(RuntimeError, match="server returned empty connector"):
        await ns.update(id_="conn-1", tags=["tag"])


@pytest.mark.asyncio
async def test_delete(ns: ConnectorsNamespace, mock_conn_client: AsyncMock) -> None:
    resp = connector_pb2.DeleteConnectorResponse()
    mock_conn_client.delete_connector = AsyncMock(return_value=resp)

    await ns.delete("conn-1")

    req = mock_conn_client.delete_connector.call_args[0][0]
    assert req.name == "connectors/conn-1"


@pytest.mark.asyncio
async def test_reauthorize_returns_result(ns: ConnectorsNamespace, mock_conn_client: AsyncMock) -> None:
    resp = connector_pb2.ReauthorizeConnectorResponse()
    resp.connector.CopyFrom(_make_connector())
    resp.authorization_url = "https://oauth.example.com/reauth?token=abc"
    mock_conn_client.reauthorize_connector = AsyncMock(return_value=resp)

    result = await ns.reauthorize("conn-1")

    assert isinstance(result, ReauthorizeResult)
    assert result.connector.id == "conn-1"
    assert result.authorization_url == "https://oauth.example.com/reauth?token=abc"
    req = mock_conn_client.reauthorize_connector.call_args[0][0]
    assert req.name == "connectors/conn-1"


@pytest.mark.asyncio
async def test_reauthorize_empty_response_raises(ns: ConnectorsNamespace, mock_conn_client: AsyncMock) -> None:
    resp = connector_pb2.ReauthorizeConnectorResponse()
    mock_conn_client.reauthorize_connector = AsyncMock(return_value=resp)

    with pytest.raises(RuntimeError, match="server returned empty connector"):
        await ns.reauthorize("conn-1")


@pytest.mark.asyncio
async def test_update_no_args_sends_empty_field_mask(
    ns: ConnectorsNamespace, mock_conn_client: AsyncMock
) -> None:
    resp = connector_pb2.UpdateConnectorResponse()
    resp.connector.CopyFrom(_make_connector())
    mock_conn_client.update_connector = AsyncMock(return_value=resp)

    await ns.update(id_="conn-1")

    req = mock_conn_client.update_connector.call_args[0][0]
    assert list(req.update_mask.paths) == []


@pytest.mark.asyncio
async def test_update_channel_config_without_type_is_ignored(
    ns: ConnectorsNamespace, mock_conn_client: AsyncMock
) -> None:
    resp = connector_pb2.UpdateConnectorResponse()
    resp.connector.CopyFrom(_make_connector())
    mock_conn_client.update_connector = AsyncMock(return_value=resp)

    await ns.update(id_="conn-1", channel_config={"app_id": "x"})

    req = mock_conn_client.update_connector.call_args[0][0]
    # channel_config without channel_config_type is silently ignored
    assert list(req.update_mask.paths) == []


@pytest.mark.asyncio
async def test_create_invalid_channel_config_type_raises(
    ns: ConnectorsNamespace, mock_conn_client: AsyncMock
) -> None:
    with pytest.raises(ValueError, match="Invalid channel_config_type"):
        await ns.create(
            channel_config_type="not_a_real_channel",  # type: ignore[arg-type]
            channel_config={"some_key": "some_value"},
        )


@pytest.mark.asyncio
async def test_update_invalid_channel_config_type_raises(
    ns: ConnectorsNamespace, mock_conn_client: AsyncMock
) -> None:
    with pytest.raises(ValueError, match="Invalid channel_config_type"):
        await ns.update(
            id_="conn-1",
            channel_config_type="not_a_real_channel",  # type: ignore[arg-type]
            channel_config={"some_key": "some_value"},
        )


@pytest.mark.asyncio
async def test_list_with_filter_and_order_by(
    ns: ConnectorsNamespace, mock_conn_client: AsyncMock
) -> None:
    resp = connector_pb2.ListConnectorsResponse()
    mock_conn_client.list_connectors = AsyncMock(return_value=resp)

    await ns.list(filter_='state == "active"', order_by="create_time desc")

    req = mock_conn_client.list_connectors.call_args[0][0]
    assert req.filter == 'state == "active"'
    assert req.order_by == "create_time desc"


@pytest.mark.asyncio
async def test_verify(ns: ConnectorsNamespace, mock_conn_client: AsyncMock) -> None:
    resp = connector_pb2.VerifyConnectorResponse()
    resp.connector.CopyFrom(_make_connector())
    mock_conn_client.verify_connector = AsyncMock(return_value=resp)

    result = await ns.verify("conn-1", "123456")

    assert result.id == "conn-1"
    req = mock_conn_client.verify_connector.call_args[0][0]
    assert req.name == "connectors/conn-1"
    assert req.code == "123456"
    assert req.password == ""


@pytest.mark.asyncio
async def test_verify_with_password(ns: ConnectorsNamespace, mock_conn_client: AsyncMock) -> None:
    resp = connector_pb2.VerifyConnectorResponse()
    resp.connector.CopyFrom(_make_connector())
    mock_conn_client.verify_connector = AsyncMock(return_value=resp)

    await ns.verify("conn-1", "654321", password="secret")

    req = mock_conn_client.verify_connector.call_args[0][0]
    assert req.code == "654321"
    assert req.password == "secret"


@pytest.mark.asyncio
async def test_verify_empty_response_raises(ns: ConnectorsNamespace, mock_conn_client: AsyncMock) -> None:
    resp = connector_pb2.VerifyConnectorResponse()
    mock_conn_client.verify_connector = AsyncMock(return_value=resp)

    with pytest.raises(RuntimeError, match="server returned empty connector"):
        await ns.verify("conn-1", "123456")


@pytest.mark.asyncio
async def test_detach(ns: ConnectorsNamespace, mock_conn_client: AsyncMock) -> None:
    resp = connector_pb2.DetachProvisionedResourceResponse()
    resp.connector.CopyFrom(_make_connector())
    mock_conn_client.detach_provisioned_resource = AsyncMock(return_value=resp)

    result = await ns.detach("conn-1")

    assert result.id == "conn-1"
    req = mock_conn_client.detach_provisioned_resource.call_args[0][0]
    assert req.name == "connectors/conn-1"


@pytest.mark.asyncio
async def test_detach_empty_response_raises(ns: ConnectorsNamespace, mock_conn_client: AsyncMock) -> None:
    resp = connector_pb2.DetachProvisionedResourceResponse()
    mock_conn_client.detach_provisioned_resource = AsyncMock(return_value=resp)

    with pytest.raises(RuntimeError, match="server returned empty connector"):
        await ns.detach("conn-1")


@pytest.mark.asyncio
async def test_create_managed_success(
    ns: ConnectorsNamespace,
    mock_conn_client: AsyncMock,
    mock_ops_client: AsyncMock,
) -> None:
    connector_proto = _make_connector("connectors/managed-1")

    packed = AnyProto()
    packed.Pack(connector_proto)

    op_done = Operation()
    op_done.name = "operations/op-1"
    op_done.done = True
    op_done.response.CopyFrom(packed)

    mock_conn_client.create_managed_connector = AsyncMock(return_value=op_done)

    result = await ns.create_managed("outbox_whatsapp", filters={"country": "US"})

    assert result.id == "managed-1"
    req = mock_conn_client.create_managed_connector.call_args[0][0]
    assert req.channel == "outbox_whatsapp"
    assert req.filters["country"] == "US"


@pytest.mark.asyncio
async def test_create_managed_polls_until_done(
    ns: ConnectorsNamespace,
    mock_conn_client: AsyncMock,
    mock_ops_client: AsyncMock,
) -> None:
    connector_proto = _make_connector("connectors/managed-2")
    packed = AnyProto()
    packed.Pack(connector_proto)

    op_pending = Operation()
    op_pending.name = "operations/op-2"
    op_pending.done = False

    op_done = Operation()
    op_done.name = "operations/op-2"
    op_done.done = True
    op_done.response.CopyFrom(packed)

    mock_conn_client.create_managed_connector = AsyncMock(return_value=op_pending)
    mock_ops_client.get_operation = AsyncMock(return_value=op_done)

    result = await ns.create_managed("outbox_sms")

    assert result.id == "managed-2"
    mock_ops_client.get_operation.assert_called_once()


@pytest.mark.asyncio
async def test_create_managed_error_raises(
    ns: ConnectorsNamespace,
    mock_conn_client: AsyncMock,
    mock_ops_client: AsyncMock,
) -> None:
    from google.rpc.status_pb2 import Status

    op_error = Operation()
    op_error.name = "operations/op-err"
    op_error.done = True
    op_error.error.CopyFrom(Status(code=9, message="quota exceeded"))

    mock_conn_client.create_managed_connector = AsyncMock(return_value=op_error)

    with pytest.raises(RuntimeError, match="quota exceeded"):
        await ns.create_managed("outbox_sms")


@pytest.mark.asyncio
async def test_create_managed_cancelled(
    ns: ConnectorsNamespace, mock_conn_client: AsyncMock, mock_ops_client: AsyncMock
) -> None:
    """Cancellation during polling propagates as CancelledError."""
    import asyncio

    op_proto = Operation()
    op_proto.done = False
    op_proto.name = "operations/op1"
    mock_conn_client.create_managed_connector = AsyncMock(return_value=op_proto)
    mock_ops_client.get_operation = AsyncMock(side_effect=asyncio.CancelledError)

    with pytest.raises(asyncio.CancelledError):
        await ns.create_managed(channel="sms")


@pytest.mark.asyncio
async def test_activate_success(ns: ConnectorsNamespace, mock_conn_client: AsyncMock) -> None:
    resp = connector_pb2.ActivateConnectorResponse()
    resp.connector.CopyFrom(_make_connector())
    mock_conn_client.activate_connector = AsyncMock(return_value=resp)

    result = await ns.activate("conn-1")

    assert result.id == "conn-1"
    req = mock_conn_client.activate_connector.call_args[0][0]
    assert req.name == "connectors/conn-1"


@pytest.mark.asyncio
async def test_activate_empty_response_raises(ns: ConnectorsNamespace, mock_conn_client: AsyncMock) -> None:
    resp = connector_pb2.ActivateConnectorResponse()
    mock_conn_client.activate_connector = AsyncMock(return_value=resp)

    with pytest.raises(RuntimeError, match="server returned empty connector"):
        await ns.activate("conn-1")


@pytest.mark.asyncio
async def test_deactivate_success(ns: ConnectorsNamespace, mock_conn_client: AsyncMock) -> None:
    resp = connector_pb2.DeactivateConnectorResponse()
    resp.connector.CopyFrom(_make_connector())
    mock_conn_client.deactivate_connector = AsyncMock(return_value=resp)

    result = await ns.deactivate("conn-1")

    assert result.id == "conn-1"
    req = mock_conn_client.deactivate_connector.call_args[0][0]
    assert req.name == "connectors/conn-1"


@pytest.mark.asyncio
async def test_deactivate_empty_response_raises(ns: ConnectorsNamespace, mock_conn_client: AsyncMock) -> None:
    resp = connector_pb2.DeactivateConnectorResponse()
    mock_conn_client.deactivate_connector = AsyncMock(return_value=resp)

    with pytest.raises(RuntimeError, match="server returned empty connector"):
        await ns.deactivate("conn-1")


@pytest.mark.asyncio
async def test_create_managed_unpack_failure(
    ns: ConnectorsNamespace, mock_conn_client: AsyncMock, mock_ops_client: AsyncMock
) -> None:
    """RuntimeError raised when op.response.Unpack returns False."""
    from google.protobuf.any_pb2 import Any as AnyProto

    op_proto = Operation()
    op_proto.done = True
    # Set a response that will fail to unpack as Connector
    any_val = AnyProto()
    any_val.Pack(Operation())  # Wrong type — Unpack to Connector will return False
    op_proto.response.CopyFrom(any_val)
    mock_conn_client.create_managed_connector = AsyncMock(return_value=op_proto)

    with pytest.raises(RuntimeError, match="failed to unpack"):
        await ns.create_managed(channel="sms")


@pytest.mark.asyncio
async def test_update_connector_webhook_url(ns: ConnectorsNamespace, mock_conn_client: AsyncMock) -> None:
    resp = connector_pb2.UpdateConnectorResponse()
    resp.connector.CopyFrom(_make_connector())
    mock_conn_client.update_connector = AsyncMock(return_value=resp)

    await ns.update(id_="conn-1", webhook_url="https://example.com/hook")

    req = mock_conn_client.update_connector.call_args[0][0]
    assert req.connector.webhook_url == "https://example.com/hook"
    assert "webhook_url" in list(req.update_mask.paths)


@pytest.mark.asyncio
async def test_update_connector_clears_webhook_url(ns: ConnectorsNamespace, mock_conn_client: AsyncMock) -> None:
    resp = connector_pb2.UpdateConnectorResponse()
    resp.connector.CopyFrom(_make_connector())
    mock_conn_client.update_connector = AsyncMock(return_value=resp)

    await ns.update(id_="conn-1", webhook_url="")

    req = mock_conn_client.update_connector.call_args[0][0]
    assert req.connector.webhook_url == ""
    assert "webhook_url" in list(req.update_mask.paths)


@pytest.mark.asyncio
async def test_verify_malformed_connector_name_in_response(
    ns: ConnectorsNamespace, mock_conn_client: AsyncMock
) -> None:
    resp = connector_pb2.VerifyConnectorResponse()
    resp.connector.name = "connectors/"  # malformed — parse_id raises ValueError on empty last segment
    mock_conn_client.verify_connector = AsyncMock(return_value=resp)

    with pytest.raises((ValueError, RuntimeError)):
        await ns.verify("conn-1", code="123456")


@pytest.mark.asyncio
async def test_create_managed_forwards_webhook_url_and_tags(
    ns: ConnectorsNamespace, mock_conn_client: AsyncMock, mock_ops_client: AsyncMock
) -> None:
    from google.protobuf.any_pb2 import Any as AnyProto
    from outbox.v1 import connector_pb2 as conn_pb2

    op_proto = Operation()
    op_proto.done = True
    connector_proto = conn_pb2.Connector()
    connector_proto.name = "connectors/managed-1"
    any_val = AnyProto()
    any_val.Pack(connector_proto)
    op_proto.response.CopyFrom(any_val)
    mock_conn_client.create_managed_connector = AsyncMock(return_value=op_proto)

    await ns.create_managed(
        channel="sms",
        webhook_url="https://example.com/hook",
        tags=["tag1", "tag2"],
    )

    req = mock_conn_client.create_managed_connector.call_args[0][0]
    assert req.webhook_url == "https://example.com/hook"
    assert list(req.tags) == ["tag1", "tag2"]
