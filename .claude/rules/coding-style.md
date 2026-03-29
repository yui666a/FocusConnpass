# コーディングスタイル

## 命名規則

PEP 8に準拠する。

- ファイル名: snake_case (`fetch_events.py`)
- クラス名: PascalCase (`FetchEventsUseCase`)
- 関数・メソッド名: snake_case (`fetch_events`)
- 変数名: snake_case (`event_id`)
- 定数: UPPER_SNAKE_CASE (`BASE_URL`)
- パッケージ名: 短い小文字のみ (`domain`, `usecase`)

## 型ヒント

- すべての関数の引数・戻り値に型ヒントを付与する
- `from __future__ import annotations` を使用
- Optional は `X | None` 記法を使用

## docstring

- すべての公開クラス・公開関数にdocstringを付与する
- Google style docstringを使用
- プライベートメソッド（`_`prefix）は省略可

## import

- 標準ライブラリ → サードパーティ → プロジェクト内の順
- ruff の isort ルールに従う

## ruff 設定

- 型アノテーション必須
- docstring 必須（Google style）
- target-version: `py312`
- 詳細なルールセットは `pyproject.toml` の `[tool.ruff]` で定義
