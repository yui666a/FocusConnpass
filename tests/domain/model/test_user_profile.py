"""UserProfile エンティティのテスト."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from focusconnpass.domain.model.user_profile import UserProfile


class TestUserProfile:
    """UserProfile エンティティのテスト."""

    def test_create_user_profile(self) -> None:
        """UserProfileを正しく生成できる."""
        profile = UserProfile(
            interests=["Python", "LLM"],
            skill_level="intermediate",
            preferred_format="any",
            location="東京",
        )
        assert profile.interests == ["Python", "LLM"]
        assert profile.skill_level == "intermediate"
        assert profile.location == "東京"

    def test_create_user_profile_without_location(self) -> None:
        """locationなしでも生成できる."""
        profile = UserProfile(
            interests=["Go"],
            skill_level="advanced",
            preferred_format="online",
            location=None,
        )
        assert profile.location is None

    def test_user_profile_is_frozen(self) -> None:
        """UserProfileはイミュータブル."""
        profile = UserProfile(
            interests=["Python"],
            skill_level="beginner",
            preferred_format="offline",
            location=None,
        )
        with pytest.raises(ValidationError):
            profile.skill_level = "advanced"  # type: ignore[misc]
