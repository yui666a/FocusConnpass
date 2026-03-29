"""ConnpassClient のテスト."""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock

import pytest

from focusconnpass.infrastructure.api.connpass_client import ConnpassClient

SAMPLE_EVENT_JSON = {
    "id": 364,
    "title": "BPStudy#56",
    "catch": "キャッチ文",
    "description": "概要説明",
    "url": "https://bpstudy.connpass.com/event/364/",
    "image_url": "https://example.com/image.png",
    "hash_tag": "bpstudy",
    "started_at": "2012-04-17T18:30:00+09:00",
    "ended_at": "2012-04-17T20:30:00+09:00",
    "limit": 80,
    "event_type": "participation",
    "open_status": "open",
    "group": {
        "id": 1,
        "subdomain": "bpstudy",
        "title": "BPStudy",
        "url": "https://bpstudy.connpass.com/",
    },
    "address": "東京都豊島区東池袋3-1-1",
    "place": "BP オフィス",
    "lat": "35.729402000000",
    "lon": "139.718209000000",
    "owner_id": 8,
    "owner_nickname": "haru860",
    "owner_display_name": "佐藤 治夫",
    "accepted": 80,
    "waiting": 15,
    "updated_at": "2012-03-20T12:07:32+09:00",
}


def _make_mock_response(payload: dict) -> MagicMock:
    """モックレスポンスを生成する.

    Args:
        payload: レスポンスとして返す dict。

    Returns:
        json() が payload を返す MagicMock。
    """
    mock_response = MagicMock()
    mock_response.json.return_value = payload
    mock_response.raise_for_status = MagicMock()
    return mock_response


@pytest.fixture()
def mock_http_client() -> MagicMock:
    """モック httpx.AsyncClient を返すフィクスチャ.

    Returns:
        get メソッドが AsyncMock になっている MagicMock。
    """
    client = MagicMock()
    client.get = AsyncMock()
    return client


@pytest.mark.asyncio()
async def test_fetch_events_sends_correct_params(mock_http_client: MagicMock) -> None:
    """fetch_events が正しいクエリパラメータを送信することを確認する."""
    mock_http_client.get.return_value = _make_mock_response(
        {"events": [SAMPLE_EVENT_JSON]}
    )
    client = ConnpassClient(api_key="test-key", http_client=mock_http_client)

    events = await client.fetch_events(count=10)

    mock_http_client.get.assert_called_once()
    _, kwargs = mock_http_client.get.call_args
    params = kwargs.get("params", {})
    assert params["order"] == 2
    assert params["count"] == 10
    assert params["start"] == 1
    assert len(events) == 1


@pytest.mark.asyncio()
async def test_fetch_events_parses_event_correctly(
    mock_http_client: MagicMock,
) -> None:
    """fetch_events がイベントを正しくパースすることを確認する."""
    mock_http_client.get.return_value = _make_mock_response(
        {"events": [SAMPLE_EVENT_JSON]}
    )
    client = ConnpassClient(api_key="test-key", http_client=mock_http_client)

    events = await client.fetch_events()

    assert len(events) == 1
    event = events[0]
    assert event.id == 364
    assert event.title == "BPStudy#56"
    assert event.catch == "キャッチ文"
    assert event.description == "概要説明"
    assert event.url == "https://bpstudy.connpass.com/event/364/"
    assert event.image_url == "https://example.com/image.png"
    assert event.hash_tag == "bpstudy"
    assert event.limit == 80
    assert event.event_type == "participation"
    assert event.open_status == "open"
    assert event.address == "東京都豊島区東池袋3-1-1"
    assert event.place == "BP オフィス"
    assert event.lat == pytest.approx(35.729402)
    assert event.lon == pytest.approx(139.718209)
    assert event.owner_id == 8
    assert event.owner_nickname == "haru860"
    assert event.owner_display_name == "佐藤 治夫"
    assert event.accepted == 80
    assert event.waiting == 15
    assert event.group is not None
    assert event.group.id == 1
    assert event.group.subdomain == "bpstudy"
    assert event.group.title == "BPStudy"


@pytest.mark.asyncio()
async def test_fetch_event_detail_found(mock_http_client: MagicMock) -> None:
    """fetch_event_detail がイベントを取得できることを確認する."""
    mock_http_client.get.return_value = _make_mock_response(
        {"events": [SAMPLE_EVENT_JSON]}
    )
    client = ConnpassClient(api_key="test-key", http_client=mock_http_client)

    event = await client.fetch_event_detail(event_id=364)

    mock_http_client.get.assert_called_once()
    _, kwargs = mock_http_client.get.call_args
    params = kwargs.get("params", {})
    assert params["event_id"] == 364
    assert event is not None
    assert event.id == 364
    assert event.title == "BPStudy#56"


@pytest.mark.asyncio()
async def test_fetch_event_detail_not_found(mock_http_client: MagicMock) -> None:
    """fetch_event_detail がイベントが存在しない場合 None を返すことを確認する."""
    mock_http_client.get.return_value = _make_mock_response({"events": []})
    client = ConnpassClient(api_key="test-key", http_client=mock_http_client)

    event = await client.fetch_event_detail(event_id=99999)

    assert event is None


@pytest.mark.asyncio()
async def test_fetch_event_with_null_group(mock_http_client: MagicMock) -> None:
    """Group が null の場合でも Event を正しくパースすることを確認する."""
    event_without_group = {**SAMPLE_EVENT_JSON, "group": None}
    mock_http_client.get.return_value = _make_mock_response(
        {"events": [event_without_group]}
    )
    client = ConnpassClient(api_key="test-key", http_client=mock_http_client)

    events = await client.fetch_events()

    assert len(events) == 1
    assert events[0].group is None
