"""Shared helpers for parsing the Claude Code hook stdin JSON envelope.

Claude Code passes hook events as a JSON object on stdin, e.g.:

    {
      "hook_event_name": "PreToolUse",
      "tool_name": "Bash",
      "tool_input": { "command": "rm -rf /" },
      ...
    }

These helpers extract the text we want to scan from `tool_input` for the
PreToolUse Bash | Edit | Write | MultiEdit matchers we care about, plus the
WebFetch/Read paths used by prompt-injection detection.
"""
from __future__ import annotations

import json
import os
import sys


def is_disabled() -> bool:
    """Return True when the user has set the global kill switch."""
    return os.environ.get("CLAUDE_HARNESSES_DISABLE", "").strip() == "1"


def read_event() -> dict:
    raw = sys.stdin.read()
    if not raw.strip():
        return {}
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return {}
    return data if isinstance(data, dict) else {}


def extract_scan_text(event: dict) -> str:
    """Concatenate the strings worth scanning from a PreToolUse event."""
    tool_name = event.get("tool_name", "")
    tool_input = event.get("tool_input") or {}
    if not isinstance(tool_input, dict):
        return ""

    parts: list[str] = []

    if tool_name == "Bash":
        cmd = tool_input.get("command", "")
        if isinstance(cmd, str):
            parts.append(cmd)
    elif tool_name in {"Edit", "MultiEdit"}:
        for key in ("old_string", "new_string", "content"):
            value = tool_input.get(key)
            if isinstance(value, str):
                parts.append(value)
        edits = tool_input.get("edits")
        if isinstance(edits, list):
            for edit in edits:
                if not isinstance(edit, dict):
                    continue
                for key in ("old_string", "new_string"):
                    value = edit.get(key)
                    if isinstance(value, str):
                        parts.append(value)
    elif tool_name == "Write":
        value = tool_input.get("content")
        if isinstance(value, str):
            parts.append(value)
    elif tool_name in {"WebFetch", "WebSearch"}:
        for key in ("prompt", "query", "url"):
            value = tool_input.get(key)
            if isinstance(value, str):
                parts.append(value)
    else:
        for value in tool_input.values():
            if isinstance(value, str):
                parts.append(value)

    return "\n".join(parts)


def emit_block(reason: str) -> int:
    """Print a stable block reason to stderr and exit with code 2."""
    sys.stderr.write(f"blocked: {reason}\n")
    sys.stderr.flush()
    return 2
