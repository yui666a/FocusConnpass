"""Event エンティティ定義."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class Group(BaseModel, frozen=True):
    """イベント主催グループ."""

    id: int
    subdomain: str
    title: str
    url: str


class Event(BaseModel, frozen=True):
    """connpass イベントエンティティ."""

    id: int
    title: str
    catch: str
    description: str
    url: str
    image_url: str | None
    hash_tag: str | None
    started_at: datetime
    ended_at: datetime
    limit: int | None
    event_type: str
    open_status: str
    group: Group | None
    address: str | None
    place: str | None
    lat: float | None
    lon: float | None
    owner_id: int
    owner_nickname: str
    owner_display_name: str
    accepted: int
    waiting: int
    updated_at: datetime
