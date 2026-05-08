#!/usr/bin/env python3
"""PreToolUse guard that blocks tool calls likely to expose hard-coded secrets.

Reads the Claude Code hook JSON envelope from stdin, scans Bash commands and
Edit/Write content for common secret patterns, and exits with code 2 to deny
the tool call when a match is found.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "_shared"))

from envelope import emit_block, extract_scan_text, is_disabled, read_event  # noqa: E402

PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("OpenAI-style API key", re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b")),
    (
        "GitHub token-like string",
        re.compile(r"\b(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9_]{30,}\b"),
    ),
    ("AWS access key id", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("private key block", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
    (
        ".env secret assignment",
        re.compile(
            r"(?im)^\s*(?:[A-Z0-9_]*SECRET|[A-Z0-9_]*TOKEN|[A-Z0-9_]*API_KEY|PASSWORD)\s*=\s*\S"
        ),
    ),
]


def find_secret(text: str) -> str | None:
    for label, pattern in PATTERNS:
        if pattern.search(text):
            return label
    return None


def main() -> int:
    if is_disabled():
        return 0

    event = read_event()
    text = extract_scan_text(event)
    if not text:
        return 0

    reason = find_secret(text)
    if reason:
        return emit_block(f"likely secret detected ({reason})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
