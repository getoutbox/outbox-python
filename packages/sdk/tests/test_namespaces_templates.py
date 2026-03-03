"""Tests for TemplatesNamespace using mocked gRPC clients."""

from __future__ import annotations

from unittest.mock import AsyncMock, patch

import pytest
from outbox.v1 import template_pb2
from outbox_sdk._enums import TemplateCategory, TemplateStatus
from outbox_sdk.namespaces._templates import ListTemplatesResult, TemplatesNamespace


def _make_template(
    connector_id: str = "conn-1",
    template_id: str = "tmpl-1",
) -> template_pb2.Template:
    t = template_pb2.Template()
    t.name = f"connectors/{connector_id}/templates/{template_id}"
    t.template_name = "order_confirmation"
    t.language = "en"
    t.category = template_pb2.Template.Category.CATEGORY_UTILITY
    t.components_json = '[{"type":"BODY","text":"Hello"}]'
    t.status = template_pb2.TemplateStatus.TEMPLATE_STATUS_APPROVED
    return t


@pytest.fixture
def mock_tmpl_client() -> AsyncMock:
    return AsyncMock()


@pytest.fixture
def ns(mock_tmpl_client: AsyncMock) -> TemplatesNamespace:
    with patch("outbox_sdk.namespaces._templates.TemplateServiceClient") as MockClient:
        MockClient.return_value = mock_tmpl_client
        return TemplatesNamespace("http://localhost:8080")


@pytest.mark.asyncio
async def test_create_success(ns: TemplatesNamespace, mock_tmpl_client: AsyncMock) -> None:
    resp = template_pb2.CreateTemplateResponse()
    resp.template.CopyFrom(_make_template())
    mock_tmpl_client.create_template = AsyncMock(return_value=resp)

    result = await ns.create(
        "conn-1",
        template_name="order_confirmation",
        language="en",
        category=TemplateCategory.UTILITY,
        components_json='[{"type":"BODY","text":"Hello"}]',
    )

    assert result.id == "tmpl-1"
    assert result.connector_id == "conn-1"
    assert result.template_name == "order_confirmation"
    assert result.language == "en"
    assert result.category == TemplateCategory.UTILITY
    assert result.status == TemplateStatus.APPROVED


@pytest.mark.asyncio
async def test_create_builds_correct_proto(ns: TemplatesNamespace, mock_tmpl_client: AsyncMock) -> None:
    resp = template_pb2.CreateTemplateResponse()
    resp.template.CopyFrom(_make_template())
    mock_tmpl_client.create_template = AsyncMock(return_value=resp)

    await ns.create(
        "conn-1",
        template_name="promo",
        language="es",
        category=TemplateCategory.MARKETING,
        components_json="[]",
    )

    req = mock_tmpl_client.create_template.call_args[0][0]
    assert req.parent == "connectors/conn-1"
    assert req.template.template_name == "promo"
    assert req.template.language == "es"
    assert req.template.category == int(TemplateCategory.MARKETING)
    assert req.template.components_json == "[]"


@pytest.mark.asyncio
async def test_create_empty_response_raises(ns: TemplatesNamespace, mock_tmpl_client: AsyncMock) -> None:
    resp = template_pb2.CreateTemplateResponse()
    mock_tmpl_client.create_template = AsyncMock(return_value=resp)

    with pytest.raises(RuntimeError, match="server returned empty template"):
        await ns.create(
            "conn-1",
            template_name="x",
            language="en",
            category=TemplateCategory.UTILITY,
            components_json="[]",
        )


@pytest.mark.asyncio
async def test_get_success(ns: TemplatesNamespace, mock_tmpl_client: AsyncMock) -> None:
    resp = template_pb2.GetTemplateResponse()
    resp.template.CopyFrom(_make_template())
    mock_tmpl_client.get_template = AsyncMock(return_value=resp)

    result = await ns.get("conn-1", "tmpl-1")

    assert result.id == "tmpl-1"
    assert result.connector_id == "conn-1"
    req = mock_tmpl_client.get_template.call_args[0][0]
    assert req.name == "connectors/conn-1/templates/tmpl-1"


@pytest.mark.asyncio
async def test_get_empty_response_raises(ns: TemplatesNamespace, mock_tmpl_client: AsyncMock) -> None:
    resp = template_pb2.GetTemplateResponse()
    mock_tmpl_client.get_template = AsyncMock(return_value=resp)

    with pytest.raises(RuntimeError, match="server returned empty template"):
        await ns.get("conn-1", "tmpl-1")


@pytest.mark.asyncio
async def test_list_returns_items(ns: TemplatesNamespace, mock_tmpl_client: AsyncMock) -> None:
    resp = template_pb2.ListTemplatesResponse()
    resp.templates.append(_make_template(template_id="tmpl-1"))
    resp.templates.append(_make_template(template_id="tmpl-2"))
    resp.next_page_token = "tok-abc"
    resp.total_size = 10
    mock_tmpl_client.list_templates = AsyncMock(return_value=resp)

    result = await ns.list("conn-1", page_size=2)

    assert isinstance(result, ListTemplatesResult)
    assert len(result.items) == 2
    assert result.items[0].id == "tmpl-1"
    assert result.items[1].id == "tmpl-2"
    assert result.next_page_token == "tok-abc"
    assert result.total_size == 10


@pytest.mark.asyncio
async def test_list_empty_next_page_token(ns: TemplatesNamespace, mock_tmpl_client: AsyncMock) -> None:
    resp = template_pb2.ListTemplatesResponse()
    resp.next_page_token = ""
    mock_tmpl_client.list_templates = AsyncMock(return_value=resp)

    result = await ns.list("conn-1")

    assert result.next_page_token is None


@pytest.mark.asyncio
async def test_list_builds_correct_proto(ns: TemplatesNamespace, mock_tmpl_client: AsyncMock) -> None:
    resp = template_pb2.ListTemplatesResponse()
    mock_tmpl_client.list_templates = AsyncMock(return_value=resp)

    await ns.list("conn-1", page_size=5, page_token="tok-xyz")

    req = mock_tmpl_client.list_templates.call_args[0][0]
    assert req.parent == "connectors/conn-1"
    assert req.page_size == 5
    assert req.page_token == "tok-xyz"


@pytest.mark.asyncio
async def test_delete(ns: TemplatesNamespace, mock_tmpl_client: AsyncMock) -> None:
    resp = template_pb2.DeleteTemplateResponse()
    mock_tmpl_client.delete_template = AsyncMock(return_value=resp)

    await ns.delete("conn-1", "tmpl-1")

    req = mock_tmpl_client.delete_template.call_args[0][0]
    assert req.name == "connectors/conn-1/templates/tmpl-1"
