#!/usr/bin/env python3
"""PreToolUse guard that flags suspected prompt-injection patterns in WebFetch/WebSearch input.

This is a heuristic. It does not catch sophisticated payloads. It does catch
common naive jailbreak prefixes like "Ignore previous instructions" that often
appear in scraped hostile content.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "_shared"))

from envelope import emit_block, extract_scan_text, is_disabled, read_event  # noqa: E402

PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    (
        "ignore previous instructions",
        re.compile(r"(?i)ignore (?:all )?(?:previous|prior|above) (?:instructions|prompts)"),
    ),
    ("disregard system prompt", re.compile(r"(?i)disregard (?:the )?system prompt")),
    (
        "you are now",
        re.compile(r"(?i)you are now (?:a |an )?(?:DAN|jailbroken|unrestricted)"),
    ),
    ("developer mode", re.compile(r"(?i)\benable developer mode\b")),
    ("reveal system prompt", re.compile(r"(?i)(?:print|reveal|show) (?:the )?system prompt")),
]


def find_injection(text: str) -> str | None:
    for label, pattern in PATTERNS:
        if pattern.search(text):
            return label
    return None


def main() -> int:
    if is_disabled():
        return 0

    event = read_event()
    if event.get("tool_name") not in {"WebFetch", "WebSearch", "Read"}:
        return 0

    text = extract_scan_text(event)
    if not text:
        return 0

    reason = find_injection(text)
    if reason:
        return emit_block(f"suspected prompt injection ({reason})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
