"""ProfileRepository インターフェース."""

from __future__ import annotations

from abc import ABC, abstractmethod

from focusconnpass.domain.model.user_profile import UserProfile


class ProfileRepository(ABC):
    """ユーザープロフィールリポジトリ."""

    @abstractmethod
    def load(self) -> UserProfile:
        """ユーザープロフィールを読み込む.

        Returns:
            ユーザープロフィール。
        """
