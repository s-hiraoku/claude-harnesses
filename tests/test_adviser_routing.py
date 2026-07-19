"""Regression coverage for deterministic Claude Adviser routing."""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = REPO_ROOT / "skills" / "adviser" / "scripts"


def _load(name: str, path: Path):  # type: ignore[no-untyped-def]
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


route_adviser = _load("route_adviser", SCRIPTS / "route_adviser.py")
run_adviser = _load("run_adviser", SCRIPTS / "run_adviser.py")


@pytest.mark.parametrize("model", ["sonnet", "opus"])
@pytest.mark.parametrize("effort", route_adviser.EFFORTS)
def test_lower_tiers_route_to_fable_at_same_effort(model: str, effort: str) -> None:
    route = route_adviser.resolve_route(model, effort)
    assert (route.target_model, route.target_effort) == ("fable", effort)


@pytest.mark.parametrize(
    ("effort", "target"),
    [("low", "medium"), ("medium", "high"), ("high", "xhigh"), ("xhigh", "max")],
)
def test_fable_routes_to_next_effort(effort: str, target: str) -> None:
    route = route_adviser.resolve_route("fable", effort)
    assert (route.target_model, route.target_effort) == ("fable", target)


def test_fable_max_fails_closed() -> None:
    with pytest.raises(route_adviser.RoutingUnavailable, match="no strictly stronger"):
        route_adviser.resolve_route("fable", "max")


def test_routing_table_covers_every_model_effort_pair() -> None:
    expected = {
        (model, effort)
        for model in route_adviser.MODEL_FAMILIES
        for effort in route_adviser.EFFORTS
    }
    assert set(route_adviser.ROUTING_TABLE) == expected


@pytest.mark.parametrize(
    ("value", "family"),
    [
        ("sonnet", "sonnet"),
        ("claude-sonnet-4-6", "sonnet"),
        ("claude-opus-4-6-20260701", "opus"),
        ("claude-fable-5", "fable"),
    ],
)
def test_model_normalization_allowlist(value: str, family: str) -> None:
    assert route_adviser.normalize_model(value) == family


@pytest.mark.parametrize(
    "value",
    ["haiku", "my-claude-fable-5", "claude-fabulous-5", "claude-opus", "fable; --help"],
)
def test_unknown_or_misleading_models_fail_closed(value: str) -> None:
    with pytest.raises(route_adviser.RoutingError):
        route_adviser.normalize_model(value)


def _write_transcript(path: Path, events: list[dict[str, object]], tail: str = "") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    content = "".join(json.dumps(event) + "\n" for event in events) + tail
    path.write_text(content, encoding="utf-8")


def test_parent_context_uses_exact_session_and_latest_assistant(tmp_path: Path) -> None:
    transcript = tmp_path / "projects" / "-repo" / "session-1.jsonl"
    _write_transcript(
        transcript,
        [
            {"type": "assistant", "message": {"model": "claude-sonnet-4-6"}},
            {
                "type": "assistant",
                "isSidechain": True,
                "message": {"model": "claude-fable-5", "role": "assistant"},
            },
            {"type": "user", "message": {"content": "switch model"}},
            {
                "type": "assistant",
                "message": {"model": "claude-opus-4-6", "role": "assistant"},
            },
        ],
        tail='{"type":"assistant",',
    )
    model, effort = route_adviser.resolve_parent_context(
        env={"CLAUDE_CODE_SESSION_ID": "session-1", "CLAUDE_EFFORT": "HIGH"},
        claude_home=tmp_path,
    )
    assert (model, effort) == ("opus", "high")


def test_ambiguous_session_fails_closed(tmp_path: Path) -> None:
    for project in ("-one", "-two"):
        _write_transcript(
            tmp_path / "projects" / project / "duplicate.jsonl",
            [{"type": "assistant", "message": {"model": "claude-fable-5"}}],
        )
    with pytest.raises(route_adviser.RoutingError, match="ambiguous"):
        route_adviser.resolve_parent_context(
            env={"CLAUDE_CODE_SESSION_ID": "duplicate", "CLAUDE_EFFORT": "medium"},
            claude_home=tmp_path,
        )


def test_symlinked_session_file_is_rejected(tmp_path: Path) -> None:
    outside = tmp_path / "outside.jsonl"
    _write_transcript(
        outside,
        [{"type": "assistant", "message": {"model": "claude-fable-5"}}],
    )
    session = tmp_path / "projects" / "-repo" / "linked.jsonl"
    session.parent.mkdir(parents=True)
    session.symlink_to(outside)
    with pytest.raises(route_adviser.RoutingError, match="no transcript"):
        route_adviser.find_session_file("linked", tmp_path)


def test_malformed_complete_transcript_line_fails_closed(tmp_path: Path) -> None:
    transcript = tmp_path / "session.jsonl"
    transcript.write_text("not-json\n", encoding="utf-8")
    with pytest.raises(route_adviser.RoutingError, match="malformed"):
        route_adviser.latest_assistant_model(transcript)


def test_missing_automatic_context_fails_closed() -> None:
    with pytest.raises(route_adviser.RoutingError, match="SESSION_ID"):
        route_adviser.resolve_parent_context(env={})
    with pytest.raises(route_adviser.RoutingError, match="CLAUDE_EFFORT"):
        route_adviser.resolve_parent_context(model="sonnet", env={})


def test_runner_command_is_explicit_and_tool_free() -> None:
    route = route_adviser.resolve_route("fable", "medium")
    command = run_adviser.build_command("/opt/claude", route)
    assert command[:7] == [
        "/opt/claude",
        "-p",
        "--model",
        "fable",
        "--effort",
        "high",
        "--output-format",
    ]
    assert "--no-session-persistence" in command
    assert "--safe-mode" in command
    turns_index = command.index("--max-turns")
    assert command[turns_index + 1] == "1"
    tools_index = command.index("--tools")
    assert command[tools_index + 1] == ""


def test_child_environment_blocks_recursion_and_removes_parent_session() -> None:
    route = route_adviser.resolve_route("sonnet", "low")
    environment = run_adviser.child_environment(
        {
            "PATH": "/bin",
            "CLAUDECODE": "1",
            "CLAUDE_CODE_SESSION_ID": "parent",
            "CLAUDE_CODE_CHILD_SESSION": "1",
            "CLAUDE_CODE_ENTRYPOINT": "sdk-cli",
            "CLAUDE_EFFORT": "low",
        },
        route,
    )
    assert environment == {
        "PATH": "/bin",
        "CLAUDE_ADVISER_CHILD": "1",
        "CLAUDE_EFFORT": "low",
    }


def _valid_stream(*, model: str = "claude-fable-5", tools: list[str] | None = None) -> str:
    events = [
        {
            "type": "system",
            "subtype": "init",
            "model": model,
            "tools": [] if tools is None else tools,
        },
        {"type": "result", "subtype": "success", "is_error": False, "result": "Review"},
    ]
    return "".join(json.dumps(event) + "\n" for event in events)


def test_stream_parser_verifies_model_tools_and_result() -> None:
    route = route_adviser.resolve_route("opus", "xhigh")
    parsed = run_adviser.parse_stream(_valid_stream(), route)
    assert parsed["effective_model"] == "claude-fable-5"
    assert parsed["requested_effort"] == "xhigh"
    assert parsed["effective_effort_verified"] is False
    assert parsed["review"] == "Review"


@pytest.mark.parametrize(
    ("stream", "message"),
    [
        (_valid_stream(model="claude-opus-4-6"), "does not match"),
        (_valid_stream(tools=["Bash"]), "tools enabled"),
        ('{"type":"result","subtype":"success","result":"Review"}\n', "one init"),
        (
            _valid_stream()
            + '{"type":"result","subtype":"success","result":"Again"}\n',
            "one result",
        ),
        ("not-json\n", "malformed"),
    ],
)
def test_stream_parser_fails_closed(stream: str, message: str) -> None:
    route = route_adviser.resolve_route("sonnet", "medium")
    with pytest.raises(run_adviser.AdviserRunError, match=message):
        run_adviser.parse_stream(stream, route)
