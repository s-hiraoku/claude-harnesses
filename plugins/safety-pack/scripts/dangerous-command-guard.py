#!/usr/bin/env python3
"""PreToolUse guard that blocks obviously dangerous shell commands."""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "_shared"))

from envelope import emit_block, extract_scan_text, is_disabled, read_event  # noqa: E402

PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("remove filesystem root", re.compile(r"\brm\s+-[^\n]*r[^\n]*f[^\n]*/(?:\s|$)")),
    (
        "remove home directory",
        re.compile(r"\brm\s+-[^\n]*r[^\n]*f[^\n]*(?:~|\$HOME)(?:\s|/|$)"),
    ),
    ("force push", re.compile(r"\bgit\s+push\b[^\n]*(?:--force|-f)\b")),
    ("hard reset", re.compile(r"\bgit\s+reset\s+--hard\b")),
    ("world-writable chmod", re.compile(r"\bchmod\s+-R\s+777\b")),
    (
        "read .env file",
        re.compile(r"\b(?:cat|less|more|tail|head|sed|awk|grep)\b[^\n]*\.env\b"),
    ),
    (
        "print private key",
        re.compile(
            r"\b(?:cat|less|more|tail|head)\b[^\n]*"
            r"(?:id_rsa|id_ed25519|private[_-]?key|\.pem)\b"
        ),
    ),
    ("dd to disk", re.compile(r"\bdd\s+[^\n]*of=/dev/(?:sd|nvme|disk)")),
    ("curl piped to shell", re.compile(r"\bcurl\b[^\n]*\|\s*(?:sh|bash|zsh|fish)\b")),
    ("wget piped to shell", re.compile(r"\bwget\b[^\n]*\|\s*(?:sh|bash|zsh|fish)\b")),
]


def find_dangerous_command(text: str) -> str | None:
    for label, pattern in PATTERNS:
        if pattern.search(text):
            return label
    return None


def main() -> int:
    if is_disabled():
        return 0

    event = read_event()
    if event.get("tool_name") != "Bash":
        return 0

    text = extract_scan_text(event)
    if not text:
        return 0

    reason = find_dangerous_command(text)
    if reason:
        return emit_block(f"dangerous command detected ({reason})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
