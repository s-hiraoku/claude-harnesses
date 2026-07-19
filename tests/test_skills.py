"""Validate every skill at the repo root has matching frontmatter."""
from __future__ import annotations

import re
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILLS_ROOT = REPO_ROOT / "skills"

FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)


def _all_skills() -> list[Path]:
    return sorted(p for p in SKILLS_ROOT.iterdir() if p.is_dir())


def test_skills_root_has_skills() -> None:
    skills = _all_skills()
    assert skills, "no skills found under skills/"


def test_each_skill_has_skill_md_with_valid_frontmatter() -> None:
    failures: list[str] = []
    for skill_dir in _all_skills():
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.is_file():
            failures.append(f"{skill_dir.name}: missing SKILL.md")
            continue

        text = skill_md.read_text()
        match = FRONTMATTER_RE.match(text)
        if not match:
            failures.append(f"{skill_dir.name}: missing YAML frontmatter")
            continue

        try:
            data = yaml.safe_load(match.group(1))
        except yaml.YAMLError as exc:
            failures.append(f"{skill_dir.name}: invalid YAML ({exc})")
            continue

        if not isinstance(data, dict):
            failures.append(f"{skill_dir.name}: frontmatter must be a mapping")
            continue

        name = data.get("name")
        description = data.get("description")
        if name != skill_dir.name:
            failures.append(
                f"{skill_dir.name}: frontmatter name {name!r} must equal directory name"
            )
        if not description or not isinstance(description, str):
            failures.append(f"{skill_dir.name}: missing description")
            continue
        if "\n" in description.strip():
            failures.append(f"{skill_dir.name}: description must be a single line")

    assert not failures, "\n".join(failures)


def assert_pr_guardian_executable_audit(skill_path: Path) -> None:
    audit_path = skill_path.parent / "references" / "pr-feedback-audit.md"
    audit = audit_path.read_text()
    shell = "\n".join(
        re.findall(r"```(?:sh|bash|shell)\n(.*?)\n```", audit, re.DOTALL)
    )
    required = (
        "reviewThreads(first:100, after:$cursor)",
        "comments(first:100, after:$cursor)",
        'args+=(-f "cursor=${cursor}")',
        'if ! page="$("$GH_BIN" "${args[@]}")"; then',
        "jq -e",
        ".errors == null",
        "hasNextPage",
        "endCursor",
        "--paginate",
        "pulls/<pr>/reviews?per_page=100",
        "pulls/<pr>/comments?per_page=100",
        "issues/<pr>/comments?per_page=100",
        "commits/<head-sha>/check-runs?per_page=100",
        "check-runs/<check-run-id>/annotations?per_page=100",
        "--method POST",
        "/replies",
        "resolveReviewThread(input:{threadId:$threadId})",
    )
    assert shell.count("while :; do") >= 2
    assert shell.count('if ! page="$("$GH_BIN" "${args[@]}")"; then') >= 2
    assert shell.count("jq -e") >= 2
    for marker in required:
        assert marker in shell
    assert shell.index("--method POST") < shell.index("resolveReviewThread")


def test_pr_guardian_waits_for_current_head_review_stabilization() -> None:
    skill = SKILLS_ROOT / "pr-guardian" / "SKILL.md"
    text = skill.read_text()
    assert_pr_guardian_executable_audit(skill)

    assert "terminal review `commit_id` equals the pinned head SHA" in text
    assert "`gh pr view --json reviews` is not commit-SHA evidence" in text
    assert "Treat `success` as a convergence checkpoint" in text
    assert "reactivate a same-head PR" in text
    assert "discard all earlier review-completion and quiet-period evidence" in text
    assert (
        "fetch the head SHA, checks, merge state, review decision, comments, reviews, "
        "and all review threads twice"
    ) in text
    assert (
        "Treat bot rate limits, timeouts, and missing current-head terminal evidence as "
        "`pending external review`"
    ) in text
    audit = (SKILLS_ROOT / "pr-guardian" / "references" / "pr-feedback-audit.md").read_text()
    assert "--json headRefOid,mergeStateStatus" in audit
    assert "      headRefOid" in audit
    assert "kaizen-loop guardian run <pr-number>" in text
    assert "Never leave a guardian child process running" in text
    assert "`gh pr checks --watch` is only a CI watcher" in text


def test_pr_guardian_resolves_target_before_starting_durable_runner() -> None:
    text = (SKILLS_ROOT / "pr-guardian" / "SKILL.md").read_text()

    resolve_cli = text.index("1. Resolve the GitHub CLI")
    resolve_pr = text.index("2. Identify the pull request")
    start_runner = text.index("3. Prefer the durable guardian runner")

    assert resolve_cli < resolve_pr < start_runner
    assert "do not attempt to invoke the runner before those arguments are available" in text
    assert "must continue its current run instead of launching another guardian child" in text
