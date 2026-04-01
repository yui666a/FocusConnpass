"""ユースケースリクエストDTO."""

from __future__ import annotations

from pydantic import BaseModel


class FetchEventsRequest(BaseModel, frozen=True):
    """イベント一括取得リクエスト."""

    count: int = 100
    ymd: str | None = None


class GetEventDetailRequest(BaseModel, frozen=True):
    """イベント詳細取得リクエスト."""

    event_id: int
