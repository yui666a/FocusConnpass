"""Connpass API クライアント実装."""

from __future__ import annotations

from datetime import datetime
from typing import Any

import httpx

from focusconnpass.domain.model.event import Event, Group
from focusconnpass.domain.repository.event_gateway import EventGateway

BASE_URL = "https://connpass.com/api/v2/events/"


class ConnpassClient(EventGateway):
    """Connpass API を使用したイベント取得クライアント.

    Args:
        api_key: Connpass API キー。
        http_client: 注入する httpx.AsyncClient。省略時は都度生成する。
    """

    def __init__(
        self,
        api_key: str,
        http_client: httpx.AsyncClient | None = None,
    ) -> None:
        """初期化する.

        Args:
            api_key: Connpass API キー。
            http_client: 注入する httpx.AsyncClient。省略時は都度生成する。
        """
        self._api_key = api_key
        self._http_client = http_client

    def _get_client(self) -> httpx.AsyncClient:
        """httpx.AsyncClient を返す.

        Returns:
            注入されたクライアント、または X-API-Key ヘッダ付きの新規クライアント。
        """
        if self._http_client is not None:
            return self._http_client
        return httpx.AsyncClient(headers={"X-API-Key": self._api_key})

    async def fetch_events(self, count: int = 100) -> list[Event]:
        """直近イベントを開催日順で取得する.

        Args:
            count: 取得件数(最大100)。

        Returns:
            イベントのリスト。
        """
        client = self._get_client()
        params: dict[str, Any] = {"order": 2, "count": count, "start": 1}
        response = await client.get(BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()
        return [self._to_event(item) for item in data.get("events", [])]

    async def fetch_event_detail(self, event_id: int) -> Event | None:
        """イベント詳細を取得する.

        Args:
            event_id: イベントID。

        Returns:
            イベント。見つからない場合は None。
        """
        client = self._get_client()
        params: dict[str, Any] = {"event_id": event_id}
        response = await client.get(BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()
        events = data.get("events", [])
        if not events:
            return None
        return self._to_event(events[0])

    @staticmethod
    def _to_event(data: dict[str, Any]) -> Event:
        """API レスポンスの dict を Event エンティティに変換する.

        Args:
            data: API レスポンスのイベント dict。

        Returns:
            Event エンティティ。
        """
        group_data = data.get("group")
        group: Group | None = (
            Group(
                id=group_data["id"],
                subdomain=group_data["subdomain"],
                title=group_data["title"],
                url=group_data["url"],
            )
            if group_data
            else None
        )

        lat_raw = data.get("lat")
        lon_raw = data.get("lon")

        return Event(
            id=data["id"],
            title=data["title"],
            catch=data["catch"],
            description=data["description"],
            url=data["url"],
            image_url=data.get("image_url"),
            hash_tag=data.get("hash_tag"),
            started_at=datetime.fromisoformat(data["started_at"]),
            ended_at=datetime.fromisoformat(data["ended_at"]),
            limit=data.get("limit"),
            event_type=data["event_type"],
            open_status=data["open_status"],
            group=group,
            address=data.get("address"),
            place=data.get("place"),
            lat=float(lat_raw) if lat_raw is not None else None,
            lon=float(lon_raw) if lon_raw is not None else None,
            owner_id=data["owner_id"],
            owner_nickname=data["owner_nickname"],
            owner_display_name=data["owner_display_name"],
            accepted=data["accepted"],
            waiting=data["waiting"],
            updated_at=datetime.fromisoformat(data["updated_at"]),
        )
