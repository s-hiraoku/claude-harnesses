#!/usr/bin/env python3
"""Resolve a strictly stronger Claude Adviser route."""

from __future__ import annotations

import argparse
import json
import os
import re
from collections.abc import Mapping
from dataclasses import asdict, dataclass
from pathlib import Path

EFFORTS = ("low", "medium", "high", "xhigh", "max")
MODEL_FAMILIES = ("sonnet", "opus", "fable")
CODEX_TO_CLAUDE = {"luna": "sonnet", "terra": "opus", "sol": "fable"}
ROUTING_TABLE: dict[tuple[str, str], tuple[str, str] | None] = {
    ("sonnet", "low"): ("fable", "low"),
    ("sonnet", "medium"): ("fable", "medium"),
    ("sonnet", "high"): ("fable", "high"),
    ("sonnet", "xhigh"): ("fable", "xhigh"),
    ("sonnet", "max"): ("fable", "max"),
    ("opus", "low"): ("fable", "low"),
    ("opus", "medium"): ("fable", "medium"),
    ("opus", "high"): ("fable", "high"),
    ("opus", "xhigh"): ("fable", "xhigh"),
    ("opus", "max"): ("fable", "max"),
    ("fable", "low"): ("fable", "medium"),
    ("fable", "medium"): ("fable", "high"),
    ("fable", "high"): ("fable", "xhigh"),
    ("fable", "xhigh"): ("fable", "max"),
    ("fable", "max"): None,
}
_VERSIONED_MODEL = re.compile(r"^claude-(sonnet|opus|fable)-[a-z0-9][a-z0-9.-]*$")
_SESSION_ID = re.compile(r"^[A-Za-z0-9._-]+$")


class RoutingError(RuntimeError):
    """The parent context is invalid or cannot be established safely."""


class RoutingUnavailable(RoutingError):
    """No strictly stronger route exists."""


@dataclass(frozen=True)
class AdviserRoute:
    source_model: str
    source_effort: str
    target_model: str
    target_effort: str


def normalize_model(value: str) -> str:
    """Normalize a supported Claude alias or versioned model identifier."""
    candidate = value.strip().lower()
    if candidate in MODEL_FAMILIES:
        return candidate
    match = _VERSIONED_MODEL.fullmatch(candidate)
    if match:
        return match.group(1)
    raise RoutingError(f"unsupported parent model: {value!r}")


def normalize_effort(value: str) -> str:
    """Normalize an allowlisted Claude effort."""
    candidate = value.strip().lower()
    if candidate not in EFFORTS:
        raise RoutingError(f"unsupported parent effort: {value!r}")
    return candidate


def resolve_route(model: str, effort: str) -> AdviserRoute:
    """Apply the complete strictly-stronger routing table."""
    source_model = normalize_model(model)
    source_effort = normalize_effort(effort)

    target = ROUTING_TABLE[(source_model, source_effort)]
    if target is None:
        raise RoutingUnavailable("fable/max has no strictly stronger Adviser route")
    return AdviserRoute(source_model, source_effort, *target)


def find_session_file(session_id: str, claude_home: Path) -> Path:
    """Find exactly one top-level project transcript for a session."""
    if not _SESSION_ID.fullmatch(session_id):
        raise RoutingError(f"invalid CLAUDE_CODE_SESSION_ID: {session_id!r}")
    projects = (claude_home / "projects").resolve()
    matches: list[Path] = []
    for path in projects.glob(f"*/{session_id}.jsonl"):
        if path.is_symlink() or not path.is_file():
            continue
        resolved = path.resolve()
        if resolved.is_relative_to(projects):
            matches.append(resolved)
    matches.sort()
    if not matches:
        raise RoutingError(f"no transcript found for Claude session {session_id!r}")
    if len(matches) != 1:
        rendered = ", ".join(str(path) for path in matches)
        raise RoutingError(f"ambiguous transcript for Claude session {session_id!r}: {rendered}")
    return matches[0]


def latest_assistant_model(session_file: Path) -> str:
    """Read the latest complete assistant event model from a transcript snapshot."""
    content = session_file.read_text(encoding="utf-8")
    lines = content.splitlines()
    has_truncated_tail = bool(content) and not content.endswith("\n")
    latest: str | None = None

    for index, line in enumerate(lines):
        if not line.strip():
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError as exc:
            if has_truncated_tail and index == len(lines) - 1:
                continue
            raise RoutingError(f"malformed session transcript line {index + 1}") from exc
        if event.get("type") != "assistant" or event.get("isSidechain") is True:
            continue
        message = event.get("message")
        if (
            isinstance(message, dict)
            and message.get("role") in (None, "assistant")
            and isinstance(message.get("model"), str)
        ):
            latest = message["model"]

    if latest is None:
        raise RoutingError("session transcript has no complete assistant model event")
    return latest


def resolve_parent_context(
    *,
    model: str | None = None,
    effort: str | None = None,
    env: Mapping[str, str] | None = None,
    claude_home: Path | None = None,
) -> tuple[str, str]:
    """Resolve parent model and effort from explicit values or Claude runtime state."""
    environment = os.environ if env is None else env

    if model is None:
        session_id = environment.get("CLAUDE_CODE_SESSION_ID", "")
        if not session_id:
            raise RoutingError("CLAUDE_CODE_SESSION_ID is required for automatic model detection")
        home = claude_home
        if home is None:
            home = Path(environment.get("CLAUDE_CONFIG_DIR", "~/.claude")).expanduser()
        model = latest_assistant_model(find_session_file(session_id, home))

    if effort is None:
        effort = environment.get("CLAUDE_EFFORT", "")
        if not effort:
            raise RoutingError("CLAUDE_EFFORT is required for automatic effort detection")

    return normalize_model(model), normalize_effort(effort)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model")
    parser.add_argument("--effort")
    parser.add_argument("--session-id")
    parser.add_argument("--claude-home", type=Path)
    args = parser.parse_args()

    env = dict(os.environ)
    if args.session_id:
        env["CLAUDE_CODE_SESSION_ID"] = args.session_id
    try:
        model, effort = resolve_parent_context(
            model=args.model,
            effort=args.effort,
            env=env,
            claude_home=args.claude_home,
        )
        print(json.dumps(asdict(resolve_route(model, effort)), sort_keys=True))
    except RoutingError as exc:
        parser.exit(2, f"adviser routing unavailable: {exc}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
