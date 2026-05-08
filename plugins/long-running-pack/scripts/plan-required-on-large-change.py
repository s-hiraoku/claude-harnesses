#!/usr/bin/env python3
"""Require plan-mode confirmation before large Edit operations.

Counts the new-string size for an Edit/MultiEdit/Write tool call. Past a
configurable byte threshold (default 4000), the hook denies the call and asks
the user to switch to plan mode or break the change into smaller pieces.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "_shared"))

from envelope import emit_block, is_disabled, read_event  # noqa: E402

DEFAULT_LIMIT = 4000


def edit_size(event: dict) -> int:
    tool = event.get("tool_name", "")
    tool_input = event.get("tool_input") or {}
    if not isinstance(tool_input, dict):
        return 0

    if tool == "Write":
        content = tool_input.get("content")
        return len(content) if isinstance(content, str) else 0

    if tool == "Edit":
        new_string = tool_input.get("new_string")
        return len(new_string) if isinstance(new_string, str) else 0

    if tool == "MultiEdit":
        edits = tool_input.get("edits") or []
        if not isinstance(edits, list):
            return 0
        total = 0
        for edit in edits:
            if not isinstance(edit, dict):
                continue
            new_string = edit.get("new_string")
            if isinstance(new_string, str):
                total += len(new_string)
        return total

    return 0


def main() -> int:
    if is_disabled():
        return 0
    if os.environ.get("CLAUDE_HARNESSES_LARGE_EDIT_OK", "").strip() == "1":
        return 0

    event = read_event()
    if not event:
        return 0

    limit_raw = os.environ.get("CLAUDE_HARNESSES_LARGE_EDIT_BYTES", "").strip()
    try:
        limit = int(limit_raw) if limit_raw else DEFAULT_LIMIT
    except ValueError:
        limit = DEFAULT_LIMIT

    size = edit_size(event)
    if size > limit:
        return emit_block(
            f"edit of {size} bytes exceeds plan-required threshold {limit}. "
            "Break into smaller edits, or set CLAUDE_HARNESSES_LARGE_EDIT_OK=1 "
            "for the current session."
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
