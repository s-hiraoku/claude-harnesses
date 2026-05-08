"""Sanity-check settings.json presets."""
from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SETTINGS_DIR = REPO_ROOT / "settings"

PRESETS = ("strict", "default", "experimental")


def test_all_presets_present() -> None:
    for name in PRESETS:
        assert (SETTINGS_DIR / f"{name}.json").is_file(), f"missing settings/{name}.json"


def test_presets_are_valid_json_with_permissions() -> None:
    for name in PRESETS:
        data = json.loads((SETTINGS_DIR / f"{name}.json").read_text())
        assert isinstance(data, dict)
        permissions = data.get("permissions")
        assert isinstance(permissions, dict), f"{name}: missing permissions"
        deny = permissions.get("deny", [])
        assert any("git push --force" in entry for entry in deny), (
            f"{name}: deny list should reject force push"
        )
        assert any("Read(.env" in entry for entry in deny), (
            f"{name}: deny list should refuse reading .env files"
        )
