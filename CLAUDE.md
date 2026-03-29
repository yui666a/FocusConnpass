# FocusConnpass

connpass APIから直近開催イベントを取得し、ホスト側LLMが推薦を行うMCPサーバー。

## 技術スタック

- Python 3.12+
- FastMCP (mcp[cli])
- httpx / pyyaml / pydantic
- pytest / pytest-asyncio
- ruff (lint & format)

## アーキテクチャ

Clean Architecture。依存は外側→内側の一方向。

- `domain/` - エンティティ、リポジトリインターフェース（標準ライブラリとpydanticのみ）
- `usecase/` - ユースケース（domainのみに依存）
- `infrastructure/` - API/DAO実装（usecase/domainに依存）
- `tools/` - MCPツール定義（controller相当）
- `server.py` - エントリポイント + DI

## コマンド

- `uv run python -m focusconnpass.server` - MCPサーバー起動
- `uv run pytest` - テスト実行
- `uv run ruff check .` - リント
- `uv run ruff format .` - フォーマット

## ルール

詳細なコーディング規約・アーキテクチャルールは `.claude/rules/` を参照。
