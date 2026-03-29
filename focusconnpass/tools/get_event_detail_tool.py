"""get_event_detail MCPツール."""

from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from focusconnpass.usecase.dto.request import GetEventDetailRequest
from focusconnpass.usecase.get_event_detail import GetEventDetailUseCase


def register_get_event_detail_tool(
    mcp: FastMCP, usecase: GetEventDetailUseCase
) -> None:
    """get_event_detail ツールをMCPサーバーに登録する.

    Args:
        mcp: FastMCPサーバーインスタンス.
        usecase: GetEventDetailUseCase インスタンス.
    """

    @mcp.tool()
    async def get_event_detail(event_id: int) -> str:
        """特定イベントの詳細情報を取得する.

        Args:
            event_id: connpass のイベントID.

        Returns:
            イベント詳細のJSON文字列.
        """
        request = GetEventDetailRequest(event_id=event_id)
        response = await usecase.execute(request)
        return response.model_dump_json()
