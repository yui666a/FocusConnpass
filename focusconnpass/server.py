"""FocusConnpass MCPサーバーエントリポイント."""

from __future__ import annotations

import httpx
from mcp.server.fastmcp import FastMCP

from focusconnpass.config import get_api_key, get_profile_path
from focusconnpass.infrastructure.api.connpass_client import ConnpassClient
from focusconnpass.infrastructure.dao.yaml_profile_loader import YamlProfileLoader
from focusconnpass.tools.fetch_events_tool import register_fetch_events_tool
from focusconnpass.tools.get_event_detail_tool import register_get_event_detail_tool
from focusconnpass.tools.get_user_profile_tool import register_get_user_profile_tool
from focusconnpass.usecase.fetch_events import FetchEventsUseCase
from focusconnpass.usecase.get_event_detail import GetEventDetailUseCase

mcp = FastMCP("FocusConnpass")


def _setup() -> None:
    """DI組み立てとツール登録を行う."""
    api_key = get_api_key()
    http_client = httpx.AsyncClient(headers={"X-API-Key": api_key})

    # Infrastructure
    connpass_client = ConnpassClient(api_key=api_key, http_client=http_client)
    profile_loader = YamlProfileLoader(path=get_profile_path())

    # Use Cases
    fetch_events_usecase = FetchEventsUseCase(gateway=connpass_client)
    get_event_detail_usecase = GetEventDetailUseCase(gateway=connpass_client)

    # Tools
    register_fetch_events_tool(mcp, fetch_events_usecase)
    register_get_event_detail_tool(mcp, get_event_detail_usecase)
    register_get_user_profile_tool(mcp, profile_loader)


_setup()
