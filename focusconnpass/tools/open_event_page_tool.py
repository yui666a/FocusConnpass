"""open_event_page MCPツール."""

from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from focusconnpass.usecase.dto.request import GetEventDetailRequest
from focusconnpass.usecase.get_event_detail import GetEventDetailUseCase


def register_open_event_page_tool(
    mcp: FastMCP, usecase: GetEventDetailUseCase
) -> None:
    """open_event_page ツールをMCPサーバーに登録する.

    Args:
        mcp: FastMCPサーバーインスタンス.
        usecase: GetEventDetailUseCase インスタンス.
    """

    @mcp.tool()
    async def open_event_page(event_id: int) -> str:
        """イベント参加ページのURLを返す.

        ユーザーが参加したいイベントを選んだ際に呼び出してください.
        返されたURLをユーザーに提示し, ブラウザで開いて参加申し込みを行えるようにします.

        Args:
            event_id: connpass のイベントID.

        Returns:
            イベントページのURL, またはイベントが見つからない場合はエラーメッセージ.
        """
        request = GetEventDetailRequest(event_id=event_id)
        response = await usecase.execute(request)
        if response.event is None:
            return f"イベントID {event_id} が見つかりませんでした"
        return response.event.url
