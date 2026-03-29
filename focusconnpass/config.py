"""アプリケーション設定."""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

_ENV_PATH = Path(__file__).resolve().parent / ".env"
load_dotenv(_ENV_PATH)


def get_api_key() -> str:
    """Connpass APIキーを環境変数から取得する.

    Returns:
        APIキー文字列。

    Raises:
        ValueError: CONNPASS_API_KEY が設定されていない場合。
    """
    api_key = os.environ.get("CONNPASS_API_KEY", "")
    if not api_key:
        msg = "環境変数 CONNPASS_API_KEY が設定されていません"
        raise ValueError(msg)
    return api_key


def get_profile_path() -> Path:
    """プロフィールYAMLのパスを取得する.

    Returns:
        profile.yaml のパス。
    """
    return Path(__file__).resolve().parent.parent / "profile.yaml"
