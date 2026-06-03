#!/usr/bin/env python3
"""PreToolUse guard that blocks direct git push/commit to main without override.

Set CLAUDE_HARNESSES_ALLOW_MAIN=1 to acknowledge the action and bypass the guard.
"""
from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "_shared"))

from envelope import emit_block, extract_scan_text, is_disabled, read_event  # noqa: E402

PROTECTED_BRANCHES = ("main", "master", "production", "release")

PUSH_TO_PROTECTED = re.compile(
    r"\bgit\s+push\b[^\n]*\b(?:origin\s+)?(?:" + "|".join(PROTECTED_BRANCHES) + r")\b"
)
COMMIT_PATTERN = re.compile(r"\bgit\s+commit\b")


def current_branch() -> str | None:
    try:
        result = subprocess.run(
            ["git", "branch", "--show-current"],
            capture_output=True,
            text=True,
            check=False,
            timeout=2,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return None
    if result.returncode != 0:
        return None
    return result.stdout.strip() or None


def main() -> int:
    if is_disabled():
        return 0
    if os.environ.get("CLAUDE_HARNESSES_ALLOW_MAIN", "").strip() == "1":
        return 0

    event = read_event()
    if event.get("tool_name") != "Bash":
        return 0

    text = extract_scan_text(event)
    if not text or "git" not in text:
        return 0

    if PUSH_TO_PROTECTED.search(text):
        return emit_block(
            "git push targeting a protected branch "
            "(set CLAUDE_HARNESSES_ALLOW_MAIN=1 to acknowledge)"
        )

    if COMMIT_PATTERN.search(text):
        branch = current_branch()
        if branch is None:
            return emit_block(
                "git commit attempted but branch could not be determined "
                "(set CLAUDE_HARNESSES_ALLOW_MAIN=1 to acknowledge)"
            )
        if branch in PROTECTED_BRANCHES:
            return emit_block(
                f"git commit on protected branch {branch!r} "
                "(set CLAUDE_HARNESSES_ALLOW_MAIN=1 to acknowledge)"
            )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
