"""Event エンティティのテスト."""

from __future__ import annotations

from datetime import UTC, datetime

import pytest
from pydantic import ValidationError

from focusconnpass.domain.model.event import Event, Group


class TestGroup:
    """Group値オブジェクトのテスト."""

    def test_create_group(self) -> None:
        """Groupを正しく生成できる."""
        group = Group(
            id=1,
            subdomain="bpstudy",
            title="BPStudy",
            url="https://bpstudy.connpass.com/",
        )
        assert group.id == 1
        assert group.subdomain == "bpstudy"

    def test_group_is_frozen(self) -> None:
        """Groupはイミュータブル."""
        group = Group(
            id=1,
            subdomain="bpstudy",
            title="BPStudy",
            url="https://bpstudy.connpass.com/",
        )
        with pytest.raises(ValidationError):
            group.id = 2  # type: ignore[misc]


class TestEvent:
    """Event エンティティのテスト."""

    def test_create_event(self) -> None:
        """Eventを全フィールド指定で生成できる."""
        event = Event(
            id=364,
            title="BPStudy#56",
            catch="キャッチ文",
            description="概要説明",
            url="https://bpstudy.connpass.com/event/364/",
            image_url="https://example.com/image.png",
            hash_tag="bpstudy",
            started_at=datetime(2012, 4, 17, 18, 30, tzinfo=UTC),
            ended_at=datetime(2012, 4, 17, 20, 30, tzinfo=UTC),
            limit=80,
            event_type="participation",
            open_status="open",
            group=Group(
                id=1,
                subdomain="bpstudy",
                title="BPStudy",
                url="https://bpstudy.connpass.com/",
            ),
            address="東京都豊島区東池袋3-1-1",
            place="BP オフィス",
            lat=35.729402,
            lon=139.718209,
            owner_id=8,
            owner_nickname="haru860",
            owner_display_name="佐藤 治夫",
            accepted=80,
            waiting=15,
            updated_at=datetime(2012, 3, 20, 12, 7, 32, tzinfo=UTC),
        )
        assert event.id == 364
        assert event.title == "BPStudy#56"
        assert event.accepted == 80

    def test_create_event_with_optional_none(self) -> None:
        """Optionalフィールドがnoneでも生成できる."""
        event = Event(
            id=100,
            title="オンラインイベント",
            catch="",
            description="desc",
            url="https://connpass.com/event/100/",
            image_url=None,
            hash_tag=None,
            started_at=datetime(2026, 4, 1, 10, 0, tzinfo=UTC),
            ended_at=datetime(2026, 4, 1, 12, 0, tzinfo=UTC),
            limit=None,
            event_type="participation",
            open_status="open",
            group=None,
            address=None,
            place=None,
            lat=None,
            lon=None,
            owner_id=1,
            owner_nickname="user1",
            owner_display_name="User 1",
            accepted=10,
            waiting=0,
            updated_at=datetime(2026, 3, 29, 0, 0, tzinfo=UTC),
        )
        assert event.place is None
        assert event.group is None

    def test_event_is_frozen(self) -> None:
        """Eventはイミュータブル."""
        event = Event(
            id=1,
            title="test",
            catch="",
            description="",
            url="https://connpass.com/event/1/",
            image_url=None,
            hash_tag=None,
            started_at=datetime(2026, 1, 1, tzinfo=UTC),
            ended_at=datetime(2026, 1, 1, tzinfo=UTC),
            limit=None,
            event_type="participation",
            open_status="open",
            group=None,
            address=None,
            place=None,
            lat=None,
            lon=None,
            owner_id=1,
            owner_nickname="u",
            owner_display_name="U",
            accepted=0,
            waiting=0,
            updated_at=datetime(2026, 1, 1, tzinfo=UTC),
        )
        with pytest.raises(ValidationError):
            event.id = 2  # type: ignore[misc]
