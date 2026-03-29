"""EventGateway インターフェース."""

from __future__ import annotations

from abc import ABC, abstractmethod

from focusconnpass.domain.model.event import Event


class EventGateway(ABC):
    """イベント取得ゲートウェイ."""

    @abstractmethod
    async def fetch_events(self, count: int = 100) -> list[Event]:
        """直近イベントを取得する.

        Args:
            count: 取得件数(最大100)。

        Returns:
            イベントのリスト。
        """

    @abstractmethod
    async def fetch_event_detail(self, event_id: int) -> Event | None:
        """イベント詳細を取得する.

        Args:
            event_id: イベントID。

        Returns:
            イベント。見つからない場合はNone。
        """
