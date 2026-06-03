#!/usr/bin/env python3
"""Track cumulative tool calls across sessions and force a stop past a threshold.

State is persisted to ~/.claude-harnesses/cost-ledger.json on the local
machine. Every PreToolUse invocation increments the counter for the current
24h window. Past the threshold, we exit 2 to deny the tool call.

Configurable via:
  CLAUDE_HARNESSES_COST_CEILING - integer cap, default 5000.
  CLAUDE_HARNESSES_COST_PATH    - override ledger path.

The ledger is rewritten only every WRITE_EVERY calls (or when within 100 of
the ceiling) so the hot-path file I/O stays cheap on every PreToolUse.
"""
from __future__ import annotations

import contextlib
import json
import os
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "_shared"))

from envelope import emit_block, is_disabled  # noqa: E402

DEFAULT_CEILING = 5000
WINDOW_SECONDS = 24 * 60 * 60
WRITE_EVERY = 10


def ledger_path() -> Path:
    override = os.environ.get("CLAUDE_HARNESSES_COST_PATH", "").strip()
    if override:
        return Path(override).expanduser()
    return Path.home() / ".claude-harnesses" / "cost-ledger.json"


def fresh_window() -> dict:
    return {"window_start": int(time.time()), "count": 0}


def load_ledger(path: Path) -> dict:
    if not path.is_file():
        return fresh_window()
    try:
        data = json.loads(path.read_text())
    except json.JSONDecodeError:
        return fresh_window()
    if not isinstance(data, dict):
        return fresh_window()
    return data


def save_ledger(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data))


def main() -> int:
    if is_disabled():
        return 0

    with contextlib.suppress(Exception):
        sys.stdin.read()

    ceiling_raw = os.environ.get("CLAUDE_HARNESSES_COST_CEILING", "").strip()
    try:
        ceiling = int(ceiling_raw) if ceiling_raw else DEFAULT_CEILING
    except ValueError:
        ceiling = DEFAULT_CEILING

    path = ledger_path()
    data = load_ledger(path)

    now = int(time.time())
    if now - int(data.get("window_start", now)) > WINDOW_SECONDS:
        data = fresh_window()

    data["count"] = int(data.get("count", 0)) + 1

    near_ceiling = data["count"] >= ceiling - 100
    if data["count"] == 1 or data["count"] % WRITE_EVERY == 0 or near_ceiling:
        save_ledger(path, data)

    if data["count"] > ceiling:
        return emit_block(
            f"cost ceiling exceeded "
            f"({data['count']} tool calls in current 24h window, ceiling {ceiling}). "
            "Reset by deleting the ledger or raising CLAUDE_HARNESSES_COST_CEILING."
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
