"""fetch_events MCPツール."""

from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from focusconnpass.usecase.dto.request import FetchEventsRequest
from focusconnpass.usecase.fetch_events import FetchEventsUseCase


def register_fetch_events_tool(mcp: FastMCP, usecase: FetchEventsUseCase) -> None:
    """fetch_events ツールをMCPサーバーに登録する.

    Args:
        mcp: FastMCPサーバーインスタンス.
        usecase: FetchEventsUseCase インスタンス.
    """

    @mcp.tool()
    async def fetch_events(count: int = 100) -> str:
        """直近開催イベントを一括取得する.

        connpass APIから直近のイベント一覧を取得します.
        ホスト側LLMでユーザーの興味に合わせてフィルタリング・推薦してください.

        Args:
            count: 取得件数(1-100, デフォルト100).

        Returns:
            イベント一覧のJSON文字列.
        """
        request = FetchEventsRequest(count=count)
        response = await usecase.execute(request)
        return response.model_dump_json()
