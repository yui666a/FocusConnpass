"""GetEventDetailUseCase のテスト."""

from __future__ import annotations

from datetime import UTC, datetime

from focusconnpass.domain.model.event import Event
from focusconnpass.domain.repository.event_gateway import EventGateway
from focusconnpass.usecase.dto.request import GetEventDetailRequest
from focusconnpass.usecase.get_event_detail import GetEventDetailUseCase


def _make_event(event_id: int) -> Event:
    """テスト用Eventを生成する."""
    return Event(
        id=event_id,
        title=f"Event {event_id}",
        catch="",
        description="desc",
        url=f"https://connpass.com/event/{event_id}/",
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
        owner_nickname="user",
        owner_display_name="User",
        accepted=10,
        waiting=0,
        updated_at=datetime(2026, 3, 29, 0, 0, tzinfo=UTC),
    )


class FakeEventGateway(EventGateway):
    """テスト用EventGateway."""

    def __init__(self, events: list[Event]) -> None:
        """初期化."""
        self._events = events

    async def fetch_events(
        self, count: int = 100, ymd: str | None = None
    ) -> list[Event]:
        """イベント一覧を返す."""
        return self._events[:count]

    async def fetch_event_detail(self, event_id: int) -> Event | None:
        """イベント詳細を返す."""
        return next((e for e in self._events if e.id == event_id), None)


class TestGetEventDetailUseCase:
    """GetEventDetailUseCase のテスト."""

    async def test_get_event_detail_found(self) -> None:
        """存在するイベントの詳細を取得できる."""
        events = [_make_event(1), _make_event(2)]
        gateway = FakeEventGateway(events)
        usecase = GetEventDetailUseCase(gateway=gateway)

        result = await usecase.execute(GetEventDetailRequest(event_id=1))

        assert result.event is not None
        assert result.event.id == 1

    async def test_get_event_detail_not_found(self) -> None:
        """存在しないイベントIDの場合Noneが返る."""
        gateway = FakeEventGateway([])
        usecase = GetEventDetailUseCase(gateway=gateway)

        result = await usecase.execute(GetEventDetailRequest(event_id=999))

        assert result.event is None
