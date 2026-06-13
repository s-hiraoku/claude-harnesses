"""Smoke test scripts/install.sh against a temporary target directory."""
from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
INSTALL_SH = REPO_ROOT / "scripts" / "install.sh"


@pytest.fixture
def target(tmp_path: Path) -> Path:
    return tmp_path


def _run_install(target: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["bash", str(INSTALL_SH), "--target", str(target), *args],
        capture_output=True,
        text=True,
        check=False,
        timeout=30,
    )


def test_install_claude_md_and_settings(target: Path) -> None:
    result = _run_install(
        target,
        "--claude-md",
        "strict",
        "--settings",
        "default",
        "--no-verify",
    )
    assert result.returncode == 0, result.stderr
    assert (target / "CLAUDE.md").is_file()
    settings = json.loads((target / ".claude" / "settings.json").read_text())
    assert settings["permissions"]["defaultMode"] == "default"


def test_install_skills_subset(target: Path) -> None:
    result = _run_install(target, "--skills", "review,tdd", "--no-verify")
    assert result.returncode == 0, result.stderr
    assert (target / ".claude" / "skills" / "review" / "SKILL.md").is_file()
    assert (target / ".claude" / "skills" / "tdd" / "SKILL.md").is_file()


def test_install_pack_merges_hooks(target: Path) -> None:
    if not shutil.which("jq"):
        pytest.skip("jq not installed")
    result = _run_install(
        target,
        "--settings",
        "default",
        "--pack",
        "safety",
        "--no-verify",
    )
    assert result.returncode == 0, result.stderr
    settings = json.loads((target / ".claude" / "settings.json").read_text())
    pre = settings.get("hooks", {}).get("PreToolUse", [])
    assert pre, "PreToolUse hooks should be merged into settings.json"
    flat_commands = [
        h["command"]
        for entry in pre
        for h in entry.get("hooks", [])
        if "command" in h
    ]
    assert any("secret-guard.py" in c for c in flat_commands), flat_commands


def test_install_product_and_research_packs(target: Path) -> None:
    result = _run_install(
        target,
        "--pack",
        "product",
        "--pack",
        "research",
        "--no-verify",
    )
    assert result.returncode == 0, result.stderr
    assert (target / ".claude" / "skills" / "frontend-design" / "SKILL.md").is_file()
    assert (target / ".claude" / "skills" / "jina-reader" / "SKILL.md").is_file()
    assert (target / ".claude" / "skills" / "jina-reader" / "scripts" / "read_url.py").is_file()
    assert (target / ".claude" / "commands" / "kaizen-loop.md").is_file()
    assert (target / ".claude" / "commands" / "jina-reader.md").is_file()


def test_install_dry_run_does_not_write(target: Path) -> None:
    result = _run_install(
        target,
        "--claude-md",
        "library",
        "--settings",
        "default",
        "--dry-run",
        "--no-verify",
    )
    assert result.returncode == 0, result.stderr
    assert not (target / "CLAUDE.md").exists()
    assert not (target / ".claude").exists()
