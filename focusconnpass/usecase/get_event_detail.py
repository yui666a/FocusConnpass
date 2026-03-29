"""イベント詳細取得ユースケース."""

from __future__ import annotations

from focusconnpass.domain.repository.event_gateway import EventGateway
from focusconnpass.usecase.dto.request import GetEventDetailRequest
from focusconnpass.usecase.dto.response import GetEventDetailResponse


class GetEventDetailUseCase:
    """特定イベントの詳細情報を取得する."""

    def __init__(self, gateway: EventGateway) -> None:
        """初期化.

        Args:
            gateway: イベント取得ゲートウェイ。
        """
        self._gateway = gateway

    async def execute(self, request: GetEventDetailRequest) -> GetEventDetailResponse:
        """ユースケースを実行する.

        Args:
            request: リクエストDTO。

        Returns:
            イベント詳細を含むレスポンス。
        """
        event = await self._gateway.fetch_event_detail(event_id=request.event_id)
        return GetEventDetailResponse(event=event)
