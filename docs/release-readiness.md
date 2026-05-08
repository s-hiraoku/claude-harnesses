# Release Readiness

Before tagging a claude-harnesses release:

- [ ] `bash scripts/verify.sh` passes (lint + tests + mkdocs strict).
- [ ] `bash scripts/validate-plugins.sh` passes.
- [ ] `bash scripts/shellcheck-all.sh` passes (if shellcheck installed).
- [ ] CHANGELOG.md has a dated entry for the new release.
- [ ] At least one example layout has been installed and dogfooded since the last release.
- [ ] Plugin schema in `schemas/plugin.schema.json` matches Claude Code's documented shape (re-check by fetching `anthropics/claude-plugins-official`).

## Versioning

Each plugin's `plugin.json` carries its own `version`. Bump the changed pack(s) only.
