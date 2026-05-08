#!/usr/bin/env python3
"""PreToolUse guard that enforces an allowlist for MCP tool calls.

Reads CLAUDE_HARNESSES_MCP_ALLOW (comma-separated list of mcp__server__tool
patterns) and blocks any MCP tool call that is not on the list. Read-only
servers can be allowed wholesale by listing the server prefix, e.g.
`mcp__github__*`.
"""
from __future__ import annotations

import fnmatch
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "_shared"))

from envelope import emit_block, is_disabled, read_event  # noqa: E402


def parse_allowlist() -> list[str]:
    raw = os.environ.get("CLAUDE_HARNESSES_MCP_ALLOW", "").strip()
    if not raw:
        return []
    return [item.strip() for item in raw.split(",") if item.strip()]


def main() -> int:
    if is_disabled():
        return 0

    event = read_event()
    tool_name = event.get("tool_name", "")
    if not tool_name.startswith("mcp__"):
        return 0

    allowlist = parse_allowlist()
    if not allowlist:
        return emit_block(
            f"MCP tool {tool_name!r} called with no CLAUDE_HARNESSES_MCP_ALLOW configured"
        )

    for pattern in allowlist:
        if fnmatch.fnmatch(tool_name, pattern):
            return 0

    return emit_block(f"MCP tool {tool_name!r} not in CLAUDE_HARNESSES_MCP_ALLOW")


if __name__ == "__main__":
    raise SystemExit(main())
