"""YAML プロフィール読み込み."""

from __future__ import annotations

from pathlib import Path

import yaml

from focusconnpass.domain.model.user_profile import UserProfile
from focusconnpass.domain.repository.profile_repository import ProfileRepository

DEFAULT_PROFILE = UserProfile(
    interests=[],
    skill_level="beginner",
    preferred_format="any",
    location=None,
)


class YamlProfileLoader(ProfileRepository):
    """YAMLファイルからユーザープロフィールを読み込む."""

    def __init__(self, path: Path) -> None:
        """初期化.

        Args:
            path: profile.yaml のパス.
        """
        self._path = path

    def load(self) -> UserProfile:
        """ユーザープロフィールを読み込む.

        ファイルが存在しない場合はデフォルトプロフィールを返す.

        Returns:
            ユーザープロフィール.
        """
        if not self._path.exists():
            return DEFAULT_PROFILE
        with self._path.open(encoding="utf-8") as f:
            data = yaml.safe_load(f)
        if not data:
            return DEFAULT_PROFILE
        return UserProfile(
            interests=data.get("interests", []),
            skill_level=data.get("skill_level", "beginner"),
            preferred_format=data.get("preferred_format", "any"),
            location=data.get("location"),
        )
