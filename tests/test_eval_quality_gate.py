"""Regression tests for the skill evaluation quality gate."""
from __future__ import annotations

import importlib.util
import subprocess
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPT = REPO_ROOT / "scripts" / "check-eval-coverage.py"


def _load_module():
    spec = importlib.util.spec_from_file_location("check_eval_coverage", SCRIPT)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_changed_skills_ignores_deleted_skill(monkeypatch: pytest.MonkeyPatch) -> None:
    module = _load_module()

    def fake_run(*args, **kwargs):
        return subprocess.CompletedProcess(
            args=args,
            returncode=0,
            stdout="\n".join(
                [
                    "M\tskills/meta-packager/SKILL.md",
                    "D\tskills/meta-promote/SKILL.md",
                    "M\tdocs/skills/meta-packager.md",
                ]
            ),
            stderr="",
        )

    monkeypatch.setattr(module.subprocess, "run", fake_run)

    assert module.changed_skills("origin/main") == ["meta-packager"]
