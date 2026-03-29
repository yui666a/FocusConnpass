"""UserProfile エンティティ定義."""

from __future__ import annotations

from pydantic import BaseModel


class UserProfile(BaseModel, frozen=True):
    """ユーザープロフィール."""

    interests: list[str]
    skill_level: str
    preferred_format: str
    location: str | None
