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
