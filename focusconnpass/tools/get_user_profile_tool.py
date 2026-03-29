"""get_user_profile MCPツール."""

from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from focusconnpass.domain.repository.profile_repository import ProfileRepository


def register_get_user_profile_tool(mcp: FastMCP, repository: ProfileRepository) -> None:
    """get_user_profile ツールをMCPサーバーに登録する.

    Args:
        mcp: FastMCPサーバーインスタンス.
        repository: ProfileRepository インスタンス.
    """

    @mcp.tool()
    async def get_user_profile() -> str:
        """ユーザープロフィールを取得する.

        ユーザーの興味, スキルレベル, 希望形式, 拠点情報を返します.
        イベント推薦の判断材料として使用してください.

        Returns:
            ユーザープロフィールのJSON文字列.
        """
        profile = repository.load()
        return profile.model_dump_json()
