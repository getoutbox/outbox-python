# packages/sdk/src/outbox_sdk/namespaces/_templates.py
from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from outbox.v1.template_connect import TemplateServiceClient
from outbox.v1.template_pb2 import (
    CreateTemplateRequest,
    DeleteTemplateRequest,
    GetTemplateRequest,
    ListTemplatesRequest,
)
from outbox.v1.template_pb2 import Template as ProtoTemplate
from outbox_sdk._enums import TemplateCategory  # noqa: TC002
from outbox_sdk._mappers import map_template

if TYPE_CHECKING:
    from connectrpc.interceptor import Interceptor
    from outbox_sdk._types import Template


@dataclass
class ListTemplatesResult:
    items: list[Template]
    next_page_token: str | None
    total_size: int


class TemplatesNamespace:
    def __init__(self, base_url: str, interceptors: tuple[Interceptor, ...] = ()) -> None:  # type: ignore[reportUnknownParameterType]
        self._client = TemplateServiceClient(base_url, interceptors=interceptors)

    async def close(self) -> None:
        await self._client.close()

    async def create(
        self,
        connector_id: str,
        *,
        template_name: str,
        language: str,
        category: TemplateCategory,
        components_json: str,
    ) -> Template:
        proto_tmpl = ProtoTemplate(
            template_name=template_name,
            language=language,
            category=int(category),  # type: ignore[reportArgumentType]
            components_json=components_json,
        )
        req = CreateTemplateRequest(
            parent=f"connectors/{connector_id}",
            template=proto_tmpl,
        )
        res = await self._client.create_template(req)
        if not res.HasField("template"):
            msg = "create_template: server returned empty template"
            raise RuntimeError(msg)
        return map_template(res.template)

    async def get(self, connector_id: str, id_: str) -> Template:
        req = GetTemplateRequest(name=f"connectors/{connector_id}/templates/{id_}")
        res = await self._client.get_template(req)
        if not res.HasField("template"):
            msg = "get_template: server returned empty template"
            raise RuntimeError(msg)
        return map_template(res.template)

    async def list(
        self,
        connector_id: str,
        *,
        page_size: int = 0,
        page_token: str = "",
    ) -> ListTemplatesResult:
        req = ListTemplatesRequest(
            parent=f"connectors/{connector_id}",
            page_size=page_size,
            page_token=page_token,
        )
        res = await self._client.list_templates(req)
        return ListTemplatesResult(
            items=[map_template(t) for t in res.templates],
            next_page_token=res.next_page_token or None,
            total_size=res.total_size,
        )

    async def delete(self, connector_id: str, id_: str) -> None:
        req = DeleteTemplateRequest(name=f"connectors/{connector_id}/templates/{id_}")
        await self._client.delete_template(req)
