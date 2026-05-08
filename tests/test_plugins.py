"""Validate plugin manifests, marketplace index, and component cross-references."""
from __future__ import annotations

import json
from pathlib import Path

import jsonschema

REPO_ROOT = Path(__file__).resolve().parent.parent
SCHEMAS_DIR = REPO_ROOT / "schemas"
PLUGINS_DIR = REPO_ROOT / "plugins"
MARKETPLACE_PATH = REPO_ROOT / ".claude-plugin" / "marketplace.json"


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text())


def test_marketplace_validates() -> None:
    schema = _load_json(SCHEMAS_DIR / "marketplace.schema.json")
    marketplace = _load_json(MARKETPLACE_PATH)
    jsonschema.validate(marketplace, schema)


def _plugin_dirs() -> list[Path]:
    return sorted(
        p for p in PLUGINS_DIR.iterdir()
        if p.is_dir() and not p.name.startswith("_")
    )


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


def test_plugin_components_resolve() -> None:
    plugin_dirs = _plugin_dirs()
    failures: list[str] = []

    for plugin_dir in plugin_dirs:
        manifest = _load_json(plugin_dir / ".claude-plugin" / "plugin.json")
        components = manifest.get("components", {})

        for kind, paths in components.items():
            for raw in paths:
                target = (plugin_dir / raw).resolve()
                if kind == "skills":
                    if not (target / "SKILL.md").is_file():
                        failures.append(f"{plugin_dir.name}: missing SKILL.md at {target}")
                else:
                    if not target.exists():
                        failures.append(f"{plugin_dir.name}: missing {kind} target {target}")

    assert not failures, "\n".join(failures)
