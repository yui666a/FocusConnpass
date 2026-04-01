# FocusConnpass

connpass APIから直近開催イベントを取得し、ホスト側LLMがユーザーの興味に合わせて推薦を行うMCPサーバー。

## 特徴

- connpass API v2 からリアルタイムにイベント情報を取得
- ユーザープロフィール（興味・スキルレベル・希望形式・拠点）に基づく推薦
- スコアリングはホスト側LLMに委任し、MCPツールはデータ提供に徹する
- 気になるイベントの参加ページURLをワンクリックで取得

## セットアップ

### 前提条件

- Python 3.12+
- [uv](https://docs.astral.sh/uv/)
- [connpass API v2 のAPIキー](https://connpass.com/about/api/v2/)

### インストール

```bash
git clone https://github.com/yui666a/FocusConnpass.git
cd FocusConnpass
uv sync --all-extras
```

### APIキーの設定

`focusconnpass/.env` を作成:

```
CONNPASS_API_KEY=your_api_key_here
```

### プロフィールの設定

`profile.yaml` を編集して自分の興味を設定:

```yaml
interests:
  - Python
  - LLM
  - クラウドインフラ
skill_level: intermediate   # beginner | intermediate | advanced
preferred_format: any       # online | offline | any
location: 東京
```

## 使い方

### MCPサーバー起動

```bash
uv run python -m focusconnpass
```

### Claude Desktop / Claude Code での設定

```json
{
  "mcpServers": {
    "focusconnpass": {
      "command": "uv",
      "args": ["run", "--directory", "/path/to/FocusConnpass", "python", "-m", "focusconnpass"]
    }
  }
}
```

### MCPツール

| ツール名 | 説明 |
|---------|------|
| `fetch_events` | 直近開催イベントを一括取得（最大100件、`ymd`で日付指定可） |
| `get_event_detail` | 特定イベントの詳細情報を取得 |
| `get_user_profile` | ユーザープロフィールを返す |
| `open_event_page` | イベント参加ページのURLを返す |

### 想定される利用フロー

```
ユーザー: 「今参加できるおすすめイベントを教えて」

ホストLLM:
  1. get_user_profile() → プロフィール取得
  2. fetch_events(count=100, ymd="20260402") → 指定日のイベント取得
  3. プロフィール × イベント群 を自身で判断 → 上位N件を推薦理由付きで回答

ユーザー: 「2番目のイベントに参加したい」

ホストLLM:
  1. open_event_page(event_id=12345) → 参加ページURLを返す
  2. ユーザーにリンクを提示
```

## 開発

```bash
uv run pytest              # テスト実行
uv run ruff check .        # リント
uv run ruff format .       # フォーマット
```

## アーキテクチャ

Clean Architecture。依存は常に外側→内側の一方向。

```
focusconnpass/
├── domain/           # エンティティ、リポジトリインターフェース（ABC）
│   ├── model/        #   Event, UserProfile
│   └── repository/   #   EventGateway, ProfileRepository
├── usecase/          # ユースケース（domainのみに依存）
│   └── dto/          #   Request / Response DTO
├── infrastructure/   # 外部システムとの接続
│   ├── api/          #   ConnpassClient（connpass API v2）
│   └── dao/          #   YamlProfileLoader（profile.yaml）
├── tools/            # MCPツール定義（controller相当）
├── config.py         # 設定（APIキー、プロフィールパス）
└── server.py         # エントリポイント + DI組み立て
```

## 技術スタック

- [FastMCP](https://github.com/jlowin/fastmcp) - MCPサーバーSDK
- [httpx](https://www.python-httpx.org/) - async HTTPクライアント
- [pydantic](https://docs.pydantic.dev/) - データバリデーション
- [PyYAML](https://pyyaml.org/) - YAML読み込み
- [ruff](https://docs.astral.sh/ruff/) - リンター/フォーマッター
- [pytest](https://docs.pytest.org/) - テスト

## ライセンス

MIT
