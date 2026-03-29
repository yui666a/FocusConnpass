# FocusConnpass MVP 設計仕様書

## 1. 概要

connpass APIから直近開催イベントを取得し、ユーザーのプロフィールに基づいてホスト側LLMが推薦を行うMCPサーバー。

### スコープ

- **MVP:** MCPサーバーのみ（Web UIなし）
- **対象クライアント:** Claude Desktop / Cursor 等のMCPホスト環境
- **将来拡張:** Web UI（FastAPI）、ローカルリポジトリ自動分析、フィードバックループ

### 設計方針

- Clean Architecture（依存は常に外側→内側の一方向）
- stock-api（`~/Projects/cosmos/stock/stock-api/`）のディレクトリ構成を踏襲
- スコアリング判断はホスト側LLMに委ね、MCPツールはデータ提供に徹する

---

## 2. アーキテクチャ

### レイヤー構成

```
┌─────────────────────────────────────────────┐
│  Frameworks & Drivers（最外層）               │
│  - FastMCP Server (server.py)               │
│  - connpass API (HTTP Client)               │
│  - ファイルシステム (プロフィールYAML読み込み)    │
├─────────────────────────────────────────────┤
│  Interface Adapters（アダプター層）            │
│  - MCP Tool definitions (tools/)            │
│  - ConnpassClient (EventGateway実装)        │
│  - YamlProfileLoader (ProfileRepository実装) │
├─────────────────────────────────────────────┤
│  Use Cases（ユースケース層）                   │
│  - FetchEventsUseCase                       │
│  - GetEventDetailUseCase                    │
├─────────────────────────────────────────────┤
│  Entities（ドメイン層・最内層）                 │
│  - Event, UserProfile                       │
│  - EventGateway, ProfileRepository (ABC)    │
└─────────────────────────────────────────────┘
```

### 依存ルール

- **Entities:** 何にも依存しない（標準ライブラリのみ）
- **Use Cases:** Entities のみに依存
- **Interface Adapters:** Use Cases / Entities に依存
- **Frameworks & Drivers:** 全層に依存可能だが、DIで具象を注入

---

## 3. ディレクトリ構成

```
focusconnpass/
├── domain/
│   ├── model/
│   │   ├── event.py              # Event エンティティ
│   │   └── user_profile.py       # UserProfile エンティティ
│   └── repository/
│       ├── event_gateway.py      # EventGateway (ABC)
│       └── profile_repository.py # ProfileRepository (ABC)
│
├── usecase/
│   ├── fetch_events.py           # FetchEventsUseCase
│   ├── get_event_detail.py       # GetEventDetailUseCase
│   └── dto/
│       ├── request.py            # ユースケース入力DTO
│       └── response.py           # ユースケース出力DTO
│
├── infrastructure/
│   ├── api/
│   │   └── connpass_client.py    # ConnpassClient (EventGateway実装)
│   ├── dao/
│   │   └── yaml_profile_loader.py # YamlProfileLoader (ProfileRepository実装)
│   └── mock/                      # テスト用モック（将来）
│
├── tools/                         # MCPツール定義（controller相当）
│   ├── fetch_events_tool.py
│   ├── get_event_detail_tool.py
│   └── get_user_profile_tool.py
│
├── server.py                      # FastMCPエントリポイント + DI組み立て
└── config.py                      # 設定（プロフィールパス等）

profile.yaml                      # ユーザープロフィール（リポジトリルート）
pyproject.toml
```

---

## 4. ドメインモデル

### Event

```python
@dataclass(frozen=True)
class Event:
    event_id: int
    title: str
    description: str        # イベント概要
    catch: str              # キャッチコピー
    event_url: str
    started_at: datetime
    ended_at: datetime
    place: str | None       # 開催場所（オンラインの場合None）
    address: str | None
    lat: float | None
    lon: float | None
    limit: int | None       # 定員
    accepted: int           # 参加確定数
    waiting: int            # キャンセル待ち数
    event_type: str         # "participation" | "advertisement"
    series_id: int | None   # グループID
    series_title: str | None
    hash_tag: str | None
```

### UserProfile

```python
@dataclass(frozen=True)
class UserProfile:
    interests: list[str]        # 興味のあるキーワード（例: ["Python", "LLM"]）
    skill_level: str            # "beginner" | "intermediate" | "advanced"
    preferred_format: str       # "online" | "offline" | "any"
    location: str | None        # 拠点（例: "東京"）
```

### Repository / Gateway インターフェース

```python
class EventGateway(ABC):
    @abstractmethod
    async def fetch_events(self, count: int = 100) -> list[Event]:
        """直近イベントを取得"""

    @abstractmethod
    async def fetch_event_detail(self, event_id: int) -> Event | None:
        """イベント詳細を取得"""

class ProfileRepository(ABC):
    @abstractmethod
    def load(self) -> UserProfile:
        """ユーザープロフィールを読み込み"""
```

---

## 5. ユースケース

### FetchEventsUseCase

connpass APIから直近イベントを一括取得する。

- 入力: `FetchEventsRequest(count: int = 100)`
- 出力: `FetchEventsResponse(events: list[Event])`

```python
class FetchEventsUseCase:
    def __init__(self, gateway: EventGateway):
        self._gateway = gateway

    async def execute(self, request: FetchEventsRequest) -> FetchEventsResponse:
        events = await self._gateway.fetch_events(count=request.count)
        return FetchEventsResponse(events=events)
```

### GetEventDetailUseCase

特定イベントの詳細情報を取得する。

- 入力: `GetEventDetailRequest(event_id: int)`
- 出力: `GetEventDetailResponse(event: Event | None)`

```python
class GetEventDetailUseCase:
    def __init__(self, gateway: EventGateway):
        self._gateway = gateway

    async def execute(self, request: GetEventDetailRequest) -> GetEventDetailResponse:
        event = await self._gateway.fetch_event_detail(event_id=request.event_id)
        return GetEventDetailResponse(event=event)
```

### DTO

```python
# dto/request.py
@dataclass(frozen=True)
class FetchEventsRequest:
    count: int = 100

@dataclass(frozen=True)
class GetEventDetailRequest:
    event_id: int

# dto/response.py
@dataclass(frozen=True)
class FetchEventsResponse:
    events: list[Event]

@dataclass(frozen=True)
class GetEventDetailResponse:
    event: Event | None
```

---

## 6. MCPツール

### ツール一覧

| ツール名 | 説明 | 呼び出し先 |
|---|---|---|
| `fetch_events` | 直近開催イベントを一括取得 | FetchEventsUseCase |
| `get_event_detail` | 特定イベントの詳細取得 | GetEventDetailUseCase |
| `get_user_profile` | ユーザープロフィールを返す | ProfileRepository.load() |

### スコアリング方針

スコアリングはMCPサーバー側では行わず、ホスト側LLMに委ねる。ツールはデータ提供に徹する。

### 想定される利用フロー

```
ユーザー: 「今参加できるおすすめイベントを教えて」
    ↓
ホストLLM:
    1. get_user_profile() → プロフィール取得
    2. fetch_events(count=100) → 直近100件取得
    3. プロフィール × イベント群 を自身で判断 → 上位N件を推薦理由付きで回答

ユーザー: 「このイベントの詳細を教えて」
    ↓
ホストLLM:
    1. get_event_detail(event_id=12345) → 詳細取得
    2. 内容を要約して回答
```

---

## 7. インフラストラクチャ

### ConnpassClient (`infrastructure/api/connpass_client.py`)

`EventGateway`の具象実装。

- HTTPクライアント: `httpx`（async対応）
- ベースURL: `https://connpass.com/api/v2/event/`
- 直近イベント取得: `order=2`（開催日順）、`count`パラメータで件数指定
- 詳細取得: `event_id`パラメータで指定
- connpass APIレスポンスJSONから`Event`エンティティへの変換をこの層で行う
- キャッシュなし（毎回リアルタイム取得）

### YamlProfileLoader (`infrastructure/dao/yaml_profile_loader.py`)

`ProfileRepository`の具象実装。

- `profile.yaml`をリポジトリルートから読み込み、`UserProfile`に変換
- ファイルが存在しない場合はデフォルトプロフィールを返す

### profile.yaml 形式

```yaml
interests:
  - Python
  - LLM
  - クラウドインフラ
skill_level: intermediate   # beginner | intermediate | advanced
preferred_format: any       # online | offline | any
location: 東京
```

---

## 8. 技術スタック

| パッケージ | 用途 |
|---|---|
| `mcp[cli]` | FastMCP（MCPサーバー構築SDK） |
| `httpx` | async HTTPクライアント（connpass API呼び出し） |
| `pyyaml` | profile.yaml 読み込み |
| `pytest` | テスト |
| `pytest-asyncio` | asyncテスト対応 |

- Python 3.12+
- `pyproject.toml` でパッケージ管理（`uv` または `pip`）
- `ruff` でリンティング・フォーマット

### 起動方法

```bash
# MCPサーバー起動
uv run python -m focusconnpass.server
```

### Claude Desktop 設定例

```json
{
  "mcpServers": {
    "focusconnpass": {
      "command": "uv",
      "args": ["run", "python", "-m", "focusconnpass.server"],
      "cwd": "/path/to/FocusConnpass"
    }
  }
}
```

---

## 9. テスト方針

- `domain/` と `usecase/`: 純粋なユニットテスト（外部依存なし）
- `infrastructure/`: connpass APIのレスポンスをモックしたテスト
- `tools/`: MVPでは手動確認、E2Eテストは将来対応

---

## 10. 将来の拡張

| 機能 | 説明 | 優先度 |
|---|---|---|
| Web UI | FastAPI + Jinja2 による推薦結果表示画面 | 高 |
| ローカルリポジトリ自動分析 | Git/メモを分析して興味を自動推定 | 高 |
| フィードバックループ | 興味あり/なしの蓄積と推薦精度向上 | 中 |
| カレンダー連携 | Google Calendar の空き時間を参照 | 中 |
| 物理的参加判定 | 現在地と会場の距離・移動時間を計算 | 低 |
