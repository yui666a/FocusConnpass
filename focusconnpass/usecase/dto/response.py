"""ユースケースレスポンスDTO."""

from __future__ import annotations

from pydantic import BaseModel

from focusconnpass.domain.model.event import Event


class FetchEventsResponse(BaseModel, frozen=True):
    """イベント一括取得レスポンス."""

    events: list[Event]


class GetEventDetailResponse(BaseModel, frozen=True):
    """イベント詳細取得レスポンス."""

    event: Event | None
