#!/usr/bin/env python3
"""Quality gate: every modified skill must have a passing eval ledger entry.

Used by .github/workflows/eval-quality-gate.yml on PRs. The script:

  1. Lists skills/<name>/SKILL.md files changed against the base ref.
  2. For each, checks evals/<name>/ledger.md exists and has a dated entry
     newer than (or equal to) the SKILL.md modification date in the diff.
  3. Skips entirely if the PR description (passed via stdin) contains the
     literal `[skip-eval]` token.

Exit codes:
  0 — all modified skills have a recent ledger entry, or [skip-eval] used.
  1 — at least one modified skill is missing an up-to-date ledger entry.
  2 — invocation error.
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = REPO_ROOT / "skills"
EVALS_DIR = REPO_ROOT / "evals"

LEDGER_DATE_RE = re.compile(r"^- (\d{4}-\d{2}-\d{2}):", re.MULTILINE)
PASS_RE = re.compile(r"\b(?:pass|plateau|converged)\b", re.IGNORECASE)


def changed_skills(base_ref: str) -> list[str]:
    """Skills with SKILL.md changed relative to base_ref."""
    try:
        result = subprocess.run(
            ["git", "diff", "--name-only", f"{base_ref}...HEAD"],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            check=True,
        )
    except subprocess.CalledProcessError as exc:
        print(f"error: git diff failed: {exc.stderr}", file=sys.stderr)
        sys.exit(2)

    skills: list[str] = []
    for line in result.stdout.splitlines():
        parts = line.split("/")
        if len(parts) >= 3 and parts[0] == "skills" and parts[2] == "SKILL.md":
            skills.append(parts[1])
    return sorted(set(skills))


def latest_ledger_date(skill: str) -> date | None:
    ledger = EVALS_DIR / skill / "ledger.md"
    if not ledger.is_file():
        return None
    text = ledger.read_text()
    matches = LEDGER_DATE_RE.findall(text)
    if not matches:
        return None
    try:
        return max(date.fromisoformat(m) for m in matches)
    except ValueError:
        return None


def ledger_records_pass(skill: str) -> bool:
    ledger = EVALS_DIR / skill / "ledger.md"
    if not ledger.is_file():
        return False
    text = ledger.read_text()
    last_dated_lines = [
        line
        for line in text.splitlines()
        if re.match(r"^- \d{4}-\d{2}-\d{2}:", line)
    ]
    if not last_dated_lines:
        return False
    return bool(PASS_RE.search(last_dated_lines[-1]))


def skill_committed_today(skill: str) -> bool:
    skill_md = SKILLS_DIR / skill / "SKILL.md"
    if not skill_md.is_file():
        return False
    try:
        result = subprocess.run(
            ["git", "log", "-1", "--format=%cs", "--", str(skill_md)],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            check=True,
        )
    except subprocess.CalledProcessError:
        return False
    stamp = result.stdout.strip()
    if not stamp:
        return False
    try:
        commit_date = date.fromisoformat(stamp)
    except ValueError:
        return False
    return commit_date == date.today()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", default="origin/main", help="base ref to diff against")
    parser.add_argument(
        "--pr-body-file",
        type=Path,
        help="path to a file containing the PR description; checked for [skip-eval]",
    )
    args = parser.parse_args()

    if (
        args.pr_body_file
        and args.pr_body_file.is_file()
        and "[skip-eval]" in args.pr_body_file.read_text()
    ):
        print("[skip-eval] token present; quality gate bypassed")
        return 0

    modified = changed_skills(args.base)
    if not modified:
        print("no skill changes detected")
        return 0

    failures: list[str] = []
    for skill in modified:
        ledger_date = latest_ledger_date(skill)
        if ledger_date is None:
            failures.append(
                f"{skill}: no evals/{skill}/ledger.md or no dated entries"
            )
            continue
        if not ledger_records_pass(skill):
            failures.append(
                f"{skill}: latest ledger entry does not record pass / plateau / converged"
            )
            continue
        if (date.today() - ledger_date).days > 14:
            failures.append(
                f"{skill}: latest ledger entry is older than 14 days "
                f"(last {ledger_date.isoformat()}); re-run the eval"
            )
            continue
        print(f"ok: {skill} (ledger {ledger_date.isoformat()})")

    if failures:
        print("\nQuality gate failed:", file=sys.stderr)
        for f in failures:
            print(f"  - {f}", file=sys.stderr)
        print(
            "\nFix by running scripts/eval-skill.sh init/new-run for the affected "
            "skill, completing an empirical-prompt-tuning iteration, and appending a "
            "passing ledger entry. Or include [skip-eval] with justification in the "
            "PR description for trivial doc-only changes.",
            file=sys.stderr,
        )
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
