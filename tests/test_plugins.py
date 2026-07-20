"""Validate plugin manifests, the marketplace index, and install-safety invariants.

The key invariant these tests protect: a plugin must be installable from a
marketplace. When Claude Code installs a plugin it copies only that plugin's
source directory into a cache, so any component or hook path that points
*outside* the plugin root (e.g. ``../../skills/foo``) silently disappears on
install. Shared content is therefore vendored into each plugin via symlinks
that git stores as real symlinks and that Claude Code dereferences at install
time.
"""
from __future__ import annotations

import json
import os
from pathlib import Path

import jsonschema

REPO_ROOT = Path(__file__).resolve().parent.parent
SCHEMAS_DIR = REPO_ROOT / "schemas"
PLUGINS_DIR = REPO_ROOT / "plugins"
MARKETPLACE_PATH = REPO_ROOT / ".claude-plugin" / "marketplace.json"

# Component dirs auto-discovered by Claude Code at the plugin root.
AUTODISCOVER_DIRS = ("skills", "agents", "commands")


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text())


def _plugin_dirs() -> list[Path]:
    return sorted(
        p for p in PLUGINS_DIR.iterdir()
        if p.is_dir() and not p.name.startswith("_")
    )


def _escapes_plugin_root(plugin_dir: Path, target: Path) -> bool:
    """True if ``target`` resolves outside ``plugin_dir``.

    Symlinks are allowed *as long as the link itself lives inside the plugin*;
    Claude Code dereferences them and copies the target content into the cache.
    What breaks install is a path component (``..``) that walks above the
    plugin root before any symlink dereference.
    """
    rel = os.path.relpath(target, plugin_dir)
    return rel == os.pardir or rel.startswith(os.pardir + os.sep)


def test_marketplace_validates() -> None:
    schema = _load_json(SCHEMAS_DIR / "marketplace.schema.json")
    jsonschema.validate(_load_json(MARKETPLACE_PATH), schema)


def test_plugin_manifests_validate() -> None:
    schema = _load_json(SCHEMAS_DIR / "plugin.schema.json")
    plugin_dirs = _plugin_dirs()
    assert plugin_dirs, "no plugins found"

    for plugin_dir in plugin_dirs:
        manifest_path = plugin_dir / ".claude-plugin" / "plugin.json"
        assert manifest_path.is_file(), f"{plugin_dir.name}: missing plugin.json"
        manifest = _load_json(manifest_path)
        jsonschema.validate(manifest, schema)
        assert manifest["name"] == plugin_dir.name, (
            f"{plugin_dir.name}: manifest name {manifest['name']!r} mismatches dir"
        )


def test_marketplace_plugins_exist_on_disk() -> None:
    marketplace = _load_json(MARKETPLACE_PATH)
    for entry in marketplace["plugins"]:
        source = REPO_ROOT / entry["source"].lstrip("./")
        assert source.is_dir(), f"{entry['name']}: source path does not exist: {source}"
        manifest = source / ".claude-plugin" / "plugin.json"
        assert manifest.is_file(), f"{entry['name']}: missing plugin.json at {manifest}"


def test_marketplace_lists_every_plugin() -> None:
    marketplace = _load_json(MARKETPLACE_PATH)
    listed = {Path(e["source"]).name for e in marketplace["plugins"]}
    on_disk = {p.name for p in _plugin_dirs()}
    assert listed == on_disk, (
        f"marketplace.json and plugins/ disagree: "
        f"only in marketplace={listed - on_disk}, only on disk={on_disk - listed}"
    )


def test_autodiscovered_skills_resolve() -> None:
    """Every skill dir found inside a plugin must hold a real SKILL.md.

    This catches dangling symlinks (e.g. a renamed root skill) that would
    install as a broken skill.
    """
    failures: list[str] = []
    for plugin_dir in _plugin_dirs():
        skills_dir = plugin_dir / "skills"
        if not skills_dir.is_dir():
            continue
        for skill in sorted(skills_dir.iterdir()):
            if not skill.is_dir():
                continue
            if not (skill / "SKILL.md").is_file():
                failures.append(f"{plugin_dir.name}: missing SKILL.md at {skill}")
    assert not failures, "\n".join(failures)


def test_compositional_standalone_skill_bundles_dependencies() -> None:
    skills_dir = PLUGINS_DIR / "skill-kaizen-loop" / "skills"
    assert (skills_dir / "implement-to-merge-ready" / "SKILL.md").is_file()
    assert (skills_dir / "ui-imagegen-director" / "SKILL.md").is_file()


def test_no_component_escapes_plugin_root() -> None:
    """Auto-discovered component dirs and their symlinks stay inside the plugin.

    A symlink whose *target* is outside the plugin is fine (it is dereferenced
    and copied on install); a symlink that itself sits outside the plugin root,
    or a directory entry that walks above it, would not be copied.
    """
    failures: list[str] = []
    for plugin_dir in _plugin_dirs():
        for name in AUTODISCOVER_DIRS:
            comp = plugin_dir / name
            if not comp.exists():
                continue
            for entry in sorted(comp.iterdir()):
                # The link/dir entry itself must live under the plugin root.
                if _escapes_plugin_root(plugin_dir, Path(os.path.abspath(entry))):
                    failures.append(f"{plugin_dir.name}: {name}/{entry.name} escapes plugin root")
                # And it must resolve to something that exists.
                if not entry.exists():
                    failures.append(f"{plugin_dir.name}: {name}/{entry.name} is a dangling link")
    assert not failures, "\n".join(failures)


def test_hooks_scripts_resolve_inside_plugin() -> None:
    """Every command referenced by a plugin's hooks.json resolves inside it.

    Hook commands use ``${CLAUDE_PLUGIN_ROOT}`` which points at the installed
    plugin cache dir, so the referenced script must exist under the plugin
    root in the repo too.
    """
    failures: list[str] = []
    for plugin_dir in _plugin_dirs():
        manifest = _load_json(plugin_dir / ".claude-plugin" / "plugin.json")
        hooks_rel = manifest.get("hooks")
        if not hooks_rel:
            continue
        hooks_path = (plugin_dir / hooks_rel).resolve()
        if not hooks_path.is_file():
            failures.append(f"{plugin_dir.name}: hooks file missing: {hooks_path}")
            continue
        hooks = _load_json(hooks_path)
        for event_entries in hooks.values():
            for entry in event_entries:
                for hook in entry.get("hooks", []):
                    cmd = hook.get("command", "")
                    marker = "${CLAUDE_PLUGIN_ROOT}/"
                    if marker not in cmd:
                        continue
                    rel = cmd.split(marker, 1)[1].split()[0]
                    script = plugin_dir / rel
                    if not script.exists():
                        failures.append(f"{plugin_dir.name}: hook script missing: {rel}")
                    if _escapes_plugin_root(plugin_dir, Path(os.path.abspath(script))):
                        failures.append(
                            f"{plugin_dir.name}: hook script escapes plugin root: {rel}"
                        )
    assert not failures, "\n".join(failures)


def test_dependencies_resolve_within_marketplace() -> None:
    """Umbrella ``dependencies`` reference plugins that exist in the marketplace."""
    marketplace = _load_json(MARKETPLACE_PATH)
    known = {Path(e["source"]).name for e in marketplace["plugins"]}
    failures: list[str] = []
    for plugin_dir in _plugin_dirs():
        manifest = _load_json(plugin_dir / ".claude-plugin" / "plugin.json")
        for dep in manifest.get("dependencies", []):
            name = dep if isinstance(dep, str) else dep["name"]
            # Cross-marketplace deps (object form with a marketplace) are exempt.
            if isinstance(dep, dict) and dep.get("marketplace"):
                continue
            if name not in known:
                failures.append(f"{plugin_dir.name}: dependency {name!r} not in marketplace")
    assert not failures, "\n".join(failures)
