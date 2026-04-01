"""イベント一括取得ユースケース."""

from __future__ import annotations

from focusconnpass.domain.repository.event_gateway import EventGateway
from focusconnpass.usecase.dto.request import FetchEventsRequest
from focusconnpass.usecase.dto.response import FetchEventsResponse


class FetchEventsUseCase:
    """直近イベントを一括取得する."""

    def __init__(self, gateway: EventGateway) -> None:
        """初期化.

        Args:
            gateway: イベント取得ゲートウェイ。
        """
        self._gateway = gateway

    async def execute(self, request: FetchEventsRequest) -> FetchEventsResponse:
        """ユースケースを実行する.

        Args:
            request: リクエストDTO。

        Returns:
            イベント一覧を含むレスポンス。
        """
        events = await self._gateway.fetch_events(count=request.count, ymd=request.ymd)
        return FetchEventsResponse(events=events)
