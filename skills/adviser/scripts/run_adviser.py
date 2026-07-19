#!/usr/bin/env python3
"""Run a fresh, tool-free Claude Adviser on a deterministic stronger route."""

from __future__ import annotations

import argparse
import contextlib
import json
import os
import signal
import subprocess
import sys
from collections.abc import Mapping, Sequence
from dataclasses import asdict
from pathlib import Path

from route_adviser import (
    AdviserRoute,
    RoutingError,
    normalize_model,
    resolve_parent_context,
    resolve_route,
)

PROMPT_CONTRACT = """\
Act as the Adviser: an independent, review-only strategic reviewer. Return review text only.
Do not edit files, run commands, delegate, or take over execution. Review only the supplied
consultation packet. Identify incorrect assumptions, missed constraints, evidence conflicts,
likely failure modes, and the best next approach. Distinguish evidence-backed findings from
uncertainty. Be concise. End with exactly four sections: Recommendation, Critical risks,
Evidence conflicts, Completion checks.

Consultation packet:
"""
MAX_PACKET_CHARS = 200_000


class AdviserRunError(RuntimeError):
    """The isolated Adviser process failed or returned unverifiable output."""


def build_command(claude_bin: str, route: AdviserRoute) -> list[str]:
    return [
        claude_bin,
        "-p",
        "--model",
        route.target_model,
        "--effort",
        route.target_effort,
        "--output-format",
        "stream-json",
        "--verbose",
        "--no-session-persistence",
        "--safe-mode",
        "--max-turns",
        "1",
        "--tools",
        "",
    ]


def child_environment(parent: Mapping[str, str], route: AdviserRoute) -> dict[str, str]:
    """Remove nested-session markers after parent context has been resolved."""
    child = dict(parent)
    for name in (
        "CLAUDECODE",
        "CLAUDE_CODE_SESSION_ID",
        "CLAUDE_CODE_CHILD_SESSION",
        "CLAUDE_CODE_ENTRYPOINT",
    ):
        child.pop(name, None)
    child["CLAUDE_ADVISER_CHILD"] = "1"
    child["CLAUDE_EFFORT"] = route.target_effort
    return child


def parse_stream(output: str, route: AdviserRoute) -> dict[str, object]:
    events: list[dict[str, object]] = []
    for line_number, line in enumerate(output.splitlines(), start=1):
        if not line.strip():
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError as exc:
            raise AdviserRunError(f"malformed stream-json line {line_number}") from exc
        if not isinstance(event, dict):
            raise AdviserRunError(f"stream-json line {line_number} is not an object")
        events.append(event)

    init_events = [
        event
        for event in events
        if event.get("type") == "system" and event.get("subtype") == "init"
    ]
    if len(init_events) != 1:
        raise AdviserRunError(f"expected exactly one init event, received {len(init_events)}")
    init = init_events[0]
    effective_model = init.get("model")
    if not isinstance(effective_model, str):
        raise AdviserRunError("init event did not report an effective model")
    try:
        effective_family = normalize_model(effective_model)
    except RoutingError as exc:
        raise AdviserRunError(f"unsupported effective Adviser model: {effective_model!r}") from exc
    if effective_family != route.target_model:
        raise AdviserRunError(
            f"effective Adviser model {effective_model!r} does not match {route.target_model!r}"
        )
    if init.get("tools") != []:
        raise AdviserRunError("Adviser initialized with tools enabled")

    results = [event for event in events if event.get("type") == "result"]
    if len(results) != 1:
        raise AdviserRunError(f"expected exactly one result event, received {len(results)}")
    result = results[0]
    review = result.get("result")
    if result.get("subtype") != "success" or result.get("is_error") is True:
        raise AdviserRunError("Adviser returned an unsuccessful result")
    if not isinstance(review, str) or not review.strip():
        raise AdviserRunError("Adviser returned an empty review")

    return {
        "route": asdict(route),
        "effective_model": effective_model,
        "requested_effort": route.target_effort,
        "effective_effort_verified": False,
        "review": review,
    }


def terminate_process_group(process: subprocess.Popen[str]) -> None:
    try:
        os.killpg(process.pid, signal.SIGTERM)
        process.wait(timeout=2)
    except (ProcessLookupError, subprocess.TimeoutExpired):
        with contextlib.suppress(ProcessLookupError):
            os.killpg(process.pid, signal.SIGKILL)


def invoke(
    command: Sequence[str],
    prompt: str,
    *,
    env: Mapping[str, str],
    timeout_seconds: float,
) -> tuple[str, str]:
    process = subprocess.Popen(
        list(command),
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        env=dict(env),
        start_new_session=True,
    )
    try:
        stdout, stderr = process.communicate(prompt, timeout=timeout_seconds)
    except subprocess.TimeoutExpired as exc:
        terminate_process_group(process)
        raise AdviserRunError(f"Adviser timed out after {timeout_seconds:g} seconds") from exc
    if process.returncode != 0:
        detail = stderr.strip() or stdout.strip() or "no diagnostic"
        raise AdviserRunError(f"Claude Adviser exited {process.returncode}: {detail}")
    return stdout, stderr


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model")
    parser.add_argument("--effort")
    parser.add_argument("--session-id")
    parser.add_argument("--claude-home", type=Path)
    parser.add_argument("--claude-bin", default="claude")
    parser.add_argument("--timeout-seconds", type=float, default=180)
    args = parser.parse_args()

    if os.environ.get("CLAUDE_ADVISER_CHILD"):
        parser.exit(3, "adviser recursion blocked\n")
    packet = sys.stdin.read(MAX_PACKET_CHARS + 1).strip()
    if not packet:
        parser.exit(2, "consultation packet is required on stdin\n")
    if len(packet) > MAX_PACKET_CHARS:
        parser.exit(2, f"consultation packet exceeds {MAX_PACKET_CHARS} characters\n")
    if args.timeout_seconds <= 0:
        parser.exit(2, "timeout must be greater than zero\n")

    environment = dict(os.environ)
    if args.session_id:
        environment["CLAUDE_CODE_SESSION_ID"] = args.session_id
    try:
        source_model, source_effort = resolve_parent_context(
            model=args.model,
            effort=args.effort,
            env=environment,
            claude_home=args.claude_home,
        )
        route = resolve_route(source_model, source_effort)
        command = build_command(args.claude_bin, route)
        stdout, _ = invoke(
            command,
            PROMPT_CONTRACT + packet,
            env=child_environment(environment, route),
            timeout_seconds=args.timeout_seconds,
        )
        print(json.dumps(parse_stream(stdout, route), ensure_ascii=False, sort_keys=True))
    except RoutingError as exc:
        parser.exit(2, f"adviser routing unavailable: {exc}\n")
    except AdviserRunError as exc:
        parser.exit(4, f"adviser execution failed: {exc}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
