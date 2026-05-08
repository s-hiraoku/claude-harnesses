"""Smoke tests asserting the bootstrap files exist and have the expected shape."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def test_required_top_level_files_exist() -> None:
    expected = [
        "README.md",
        "LICENSE",
        "CLAUDE.md",
        "CONTRIBUTING.md",
        "SECURITY.md",
        "CHANGELOG.md",
        ".gitignore",
        "pyproject.toml",
        "requirements-dev.txt",
        "mkdocs.yml",
        "scripts/verify.sh",
        "scripts/checkpoint.sh",
        "ledger/current.md",
        "ledger/decisions.md",
        "ledger/risks.md",
        "ledger/verification.md",
        "docs/index.md",
        "docs/installation.md",
        ".github/workflows/verify.yml",
    ]
    missing = [p for p in expected if not (REPO_ROOT / p).is_file()]
    assert not missing, f"missing required files: {missing}"


def test_verify_script_uses_claude_env_var() -> None:
    content = (REPO_ROOT / "scripts" / "verify.sh").read_text()
    assert "CLAUDE_HARNESSES_STRICT" in content
    assert "CODEX_HARNESSES_STRICT" not in content


def test_claude_md_mentions_repository_principles() -> None:
    content = (REPO_ROOT / "CLAUDE.md").read_text()
    assert "Claude Code" in content
    assert "Principles" in content


def test_mkdocs_uses_material_theme() -> None:
    content = (REPO_ROOT / "mkdocs.yml").read_text()
    assert "name: material" in content
    assert "site_name: Claude Harnesses" in content


def test_readme_advertises_four_install_methods() -> None:
    content = (REPO_ROOT / "README.md").read_text()
    methods = (
        "/plugin marketplace add",
        "gh skill install",
        "npx skills add",
        "scripts/install.sh",
    )
    for method in methods:
        assert method in content, f"README missing install method: {method}"
