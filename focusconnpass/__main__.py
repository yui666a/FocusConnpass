"""python -m focusconnpass で起動するためのエントリポイント."""

from __future__ import annotations

from focusconnpass.server import mcp

mcp.run()
