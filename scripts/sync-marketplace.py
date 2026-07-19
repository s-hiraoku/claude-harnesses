#!/usr/bin/env python3
"""Generate marketplace artifacts from their sources.

Sources of truth:
  - skills/<name>/SKILL.md            (skill definitions)
  - plugins/<pack>/                   (hand-authored thematic packs)
  - .claude-plugin/marketplace.json   (pack entries only)

Generated artifacts (never edit by hand):
  - plugins/full/                     umbrella plugin: symlinks to every skill,
                                      every pack command/agent/script, merged hooks.json
  - plugins/skill-<name>/             one micro-plugin per skill
  - .claude-plugin/marketplace.json   full entry + pack entries + skill-* entries

Usage:
  python3 scripts/sync-marketplace.py          # regenerate in place
  python3 scripts/sync-marketplace.py --check  # exit 1 if anything is out of sync
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
PLUGINS = REPO / "plugins"
SKILLS = REPO / "skills"
MARKETPLACE = REPO / ".claude-plugin" / "marketplace.json"

AUTHOR = {"name": "s-hiraoku", "url": "https://github.com/s-hiraoku"}
FULL_VERSION = "0.2.0"
SKILL_PLUGIN_VERSION = "0.1.0"
HOOK_EVENT_ORDER = [
    "SessionStart",
    "UserPromptSubmit",
    "PreToolUse",
    "PostToolUse",
    "Stop",
    "SessionEnd",
]
MAX_DESCRIPTION = 200


def fail(message: str) -> None:
    print(f"sync-marketplace: {message}", file=sys.stderr)
    sys.exit(1)


def pack_dirs() -> list[Path]:
    packs = []
    for path in sorted(PLUGINS.iterdir()):
        if not path.is_dir() or path.name.startswith(("_", ".")):
            continue
        if path.name == "full" or path.name.startswith("skill-"):
            continue
        packs.append(path)
    return packs


def skill_names() -> list[str]:
    return sorted(p.name for p in SKILLS.iterdir() if (p / "SKILL.md").is_file())


def skill_description(name: str) -> str:
    text = (SKILLS / name / "SKILL.md").read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
    if not match:
        fail(f"skills/{name}/SKILL.md has no frontmatter")
    frontmatter = match.group(1)
    desc_match = re.search(
        r"^description:\s*(.+?)(?=^\S|\Z)", frontmatter, re.MULTILINE | re.DOTALL
    )
    if not desc_match:
        fail(f"skills/{name}/SKILL.md frontmatter has no description")
    description = " ".join(desc_match.group(1).split())
    if len(description) > MAX_DESCRIPTION:
        sentence = description.split(". ")[0].rstrip(".") + "."
        description = (
            sentence
            if len(sentence) <= MAX_DESCRIPTION
            else description[: MAX_DESCRIPTION - 1].rstrip() + "…"
        )
    return description


def collect_pack_files(subdir: str, suffix: str | None = None) -> dict[str, Path]:
    """Map filename -> pack dir for every pack file in <pack>/<subdir>/."""
    found: dict[str, Path] = {}
    for pack in pack_dirs():
        directory = pack / subdir
        if not directory.is_dir():
            continue
        for item in sorted(directory.iterdir()):
            if item.name == "__pycache__":
                continue
            if suffix and not item.name.endswith(suffix):
                continue
            if not item.is_file() and not item.is_symlink():
                continue
            if item.name in found:
                fail(
                    f"{subdir}/{item.name} exists in both "
                    f"{found[item.name].name} and {pack.name}; rename one"
                )
            found[item.name] = pack
    return found


def merged_hooks() -> dict:
    merged: dict[str, list] = {}
    for pack in pack_dirs():
        hooks_file = pack / "hooks.json"
        if not hooks_file.is_file():
            continue
        for event, groups in json.loads(hooks_file.read_text(encoding="utf-8")).items():
            merged.setdefault(event, []).extend(groups)
    unknown = set(merged) - set(HOOK_EVENT_ORDER)
    if unknown:
        fail(f"unknown hook events {sorted(unknown)}; extend HOOK_EVENT_ORDER")
    return {event: merged[event] for event in HOOK_EVENT_ORDER if event in merged}


def skill_bundle_text(name: str, commands: dict[str, Path]) -> str:
    """SKILL.md plus its slash command body, since delegation instructions
    (e.g. "delegate to the ci-fixer subagent") often live in the command,
    not the skill file."""
    text = (SKILLS / name / "SKILL.md").read_text(encoding="utf-8")
    command_file = commands.get(f"{name}.md")
    if command_file:
        text += (PLUGINS / command_file.name / "commands" / f"{name}.md").read_text(
            encoding="utf-8"
        )
    return text


def referenced_agents(skill: str, agents: dict[str, Path], commands: dict[str, Path]) -> list[str]:
    text = skill_bundle_text(skill, commands)
    return [name for name in sorted(agents) if name.removesuffix(".md") in text]


ALIAS_RE = re.compile(r"\balias for ([a-z][a-z0-9-]*)", re.IGNORECASE)


def alias_target(name: str) -> str | None:
    """If a skill's description declares itself a compatibility alias for
    another skill (e.g. "Compatibility alias for pr-guardian"), return that
    target skill's name so standalone installs can bundle what it delegates to.
    """
    text = (SKILLS / name / "SKILL.md").read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
    frontmatter = match.group(1) if match else ""
    found = ALIAS_RE.search(frontmatter)
    return found.group(1) if found else None


def dumps(data: dict) -> str:
    return json.dumps(data, indent=2, ensure_ascii=False) + "\n"


def build_manifest() -> dict[str, tuple[str, str]]:
    """Expected state: path (repo-relative) -> ("link", target) | ("file", content)."""
    manifest: dict[str, tuple[str, str]] = {}
    skills = skill_names()
    commands = collect_pack_files("commands", suffix=".md")
    agents = collect_pack_files("agents", suffix=".md")
    scripts = collect_pack_files("scripts")

    # --- plugins/full ---
    full = "plugins/full"
    manifest[f"{full}/_shared"] = ("link", "../_shared")
    for name in skills:
        manifest[f"{full}/skills/{name}"] = ("link", f"../../../skills/{name}")
    for filename, pack in commands.items():
        manifest[f"{full}/commands/{filename}"] = (
            "link",
            f"../../{pack.name}/commands/{filename}",
        )
    for filename, pack in agents.items():
        manifest[f"{full}/agents/{filename}"] = (
            "link",
            f"../../{pack.name}/agents/{filename}",
        )
    for filename, pack in scripts.items():
        manifest[f"{full}/scripts/{filename}"] = (
            "link",
            f"../../{pack.name}/scripts/{filename}",
        )
    manifest[f"{full}/hooks.json"] = ("file", dumps(merged_hooks()))
    manifest[f"{full}/.claude-plugin/plugin.json"] = (
        "file",
        dumps(
            {
                "name": "full",
                "version": FULL_VERSION,
                "description": (
                    "Umbrella plugin bundling every skill, command, agent, and hook "
                    "from all claude-harnesses packs in one install."
                ),
                "author": AUTHOR,
                "homepage": "https://s-hiraoku.github.io/claude-harnesses/packs/full/",
                "license": "MIT",
                "keywords": ["umbrella", "claude-harnesses"],
                "hooks": "./hooks.json",
            }
        ),
    )

    # --- plugins/skill-<name> ---
    for name in skills:
        root = f"plugins/skill-{name}"
        # A compatibility alias (e.g. finish-pr-feedback -> pr-guardian) is a
        # thin pointer that immediately delegates to another skill's workflow;
        # bundle that target's skill/command/agents too, or a standalone
        # install of the alias ships a skill with nothing to run.
        bundled = [name]
        target = alias_target(name)
        if target:
            if target not in skills:
                fail(
                    f"skills/{name}/SKILL.md declares alias target {target!r}, "
                    "which doesn't exist"
                )
            bundled.append(target)

        for bundled_name in bundled:
            manifest[f"{root}/skills/{bundled_name}"] = (
                "link",
                f"../../../skills/{bundled_name}",
            )
            command = f"{bundled_name}.md"
            if command in commands:
                manifest[f"{root}/commands/{command}"] = (
                    "link",
                    f"../../{commands[command].name}/commands/{command}",
                )
            for agent in referenced_agents(bundled_name, agents, commands):
                manifest[f"{root}/agents/{agent}"] = (
                    "link",
                    f"../../{agents[agent].name}/agents/{agent}",
                )
        manifest[f"{root}/.claude-plugin/plugin.json"] = (
            "file",
            dumps(
                {
                    "name": f"skill-{name}",
                    "version": SKILL_PLUGIN_VERSION,
                    "description": skill_description(name),
                    "author": AUTHOR,
                    "license": "MIT",
                    "keywords": ["skill", name],
                }
            ),
        )

    # --- marketplace.json ---
    current = json.loads(MARKETPLACE.read_text(encoding="utf-8"))
    pack_entries = [
        entry
        for entry in current["plugins"]
        if entry["name"] != "full" and not entry["name"].startswith("skill-")
    ]
    listed = {entry["name"] for entry in pack_entries}
    on_disk = {pack.name for pack in pack_dirs()}
    if listed != on_disk:
        fail(
            f"marketplace pack entries out of sync with plugins/: "
            f"missing {sorted(on_disk - listed)}, stale {sorted(listed - on_disk)}"
        )
    full_entry = {
        "name": "full",
        "source": "./plugins/full",
        "description": (
            "Everything at once: every skill, command, agent, and hook "
            "from all packs. Install this or individual packs, not both."
        ),
        "category": "umbrella",
        "tags": ["full", "umbrella"],
    }
    skill_entries = [
        {
            "name": f"skill-{name}",
            "source": f"./plugins/skill-{name}",
            "description": skill_description(name),
            "category": "skill",
            "tags": ["skill", name],
        }
        for name in skills
    ]
    manifest[".claude-plugin/marketplace.json"] = (
        "file",
        dumps(
            {
                "name": current["name"],
                "owner": current["owner"],
                "description": current["description"],
                "plugins": [full_entry, *pack_entries, *skill_entries],
            }
        ),
    )
    return manifest


def managed_paths() -> list[Path]:
    """Existing files under generator-owned roots (full sans README, skill-*)."""
    paths: list[Path] = []
    roots = [PLUGINS / "full", *sorted(PLUGINS.glob("skill-*"))]
    for root in roots:
        if not root.is_dir():
            continue
        for path in root.rglob("*"):
            if path.is_dir() and not path.is_symlink():
                continue
            if path == PLUGINS / "full" / "README.md":
                continue
            paths.append(path)
    return paths


def diff_manifest(manifest: dict[str, tuple[str, str]]) -> list[str]:
    problems = []
    for rel, (kind, expected) in sorted(manifest.items()):
        path = REPO / rel
        if kind == "link":
            if not path.is_symlink():
                problems.append(f"missing or not a symlink: {rel}")
            elif str(path.readlink()) != expected:
                problems.append(f"wrong symlink target: {rel} -> {path.readlink()}")
        else:
            if not path.is_file() or path.is_symlink():
                problems.append(f"missing file: {rel}")
            elif path.read_text(encoding="utf-8") != expected:
                problems.append(f"content drift: {rel}")
    expected_rels = {REPO / rel for rel in manifest}
    for path in managed_paths():
        if path not in expected_rels:
            problems.append(f"stale generated path: {path.relative_to(REPO)}")
    return problems


def apply_manifest(manifest: dict[str, tuple[str, str]]) -> None:
    expected_rels = {REPO / rel for rel in manifest}
    for path in managed_paths():
        if path not in expected_rels:
            path.unlink()
    for rel, (kind, expected) in sorted(manifest.items()):
        path = REPO / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        if kind == "link":
            if path.is_symlink() and str(path.readlink()) == expected:
                continue
            if path.is_symlink() or path.exists():
                path.unlink()
            path.symlink_to(expected)
        else:
            if (
                path.is_file()
                and not path.is_symlink()
                and path.read_text(encoding="utf-8") == expected
            ):
                continue
            path.write_text(expected, encoding="utf-8")
    # Drop now-empty directories left behind by removals.
    for root in [PLUGINS / "full", *sorted(PLUGINS.glob("skill-*"))]:
        if not root.is_dir():
            continue
        for directory in sorted(root.rglob("*"), reverse=True):
            if (
                directory.is_dir()
                and not directory.is_symlink()
                and not any(directory.iterdir())
            ):
                directory.rmdir()


def main() -> None:
    check = "--check" in sys.argv[1:]
    manifest = build_manifest()
    if check:
        problems = diff_manifest(manifest)
        if problems:
            for problem in problems:
                print(f"sync-marketplace: {problem}", file=sys.stderr)
            print(
                "sync-marketplace: run `python3 scripts/sync-marketplace.py` to fix",
                file=sys.stderr,
            )
            sys.exit(1)
        print("sync-marketplace: in sync")
    else:
        apply_manifest(manifest)
        print("sync-marketplace: regenerated plugins/full, skill-* plugins, marketplace.json")


if __name__ == "__main__":
    main()
