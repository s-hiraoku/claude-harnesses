# Risks

Use this file to track known risks during long-running work.

## Template

### YYYY-MM-DD: Risk Title

- Risk:
- Impact:
- Likelihood:
- Mitigation:
- Status:

## Open Risks

### 2026-05-08: Plugin schema drift

- Risk: Anthropic ships breaking changes to `.claude-plugin/plugin.json` shape.
- Impact: All packs become uninstallable until schema is updated.
- Likelihood: Medium (plugin marketplace is recent).
- Mitigation: Pin `schemas/plugin.schema.json` to a documented Claude Code release version in CHANGELOG; CI fails loud on validation mismatch.
- Status: Monitoring.

### 2026-05-08: Symlinks on Windows

- Risk: Skill symlinks from `plugins/*/skills/<name>` to `skills/<name>` become text files on Windows + Git without `core.symlinks=true`.
- Impact: Plugin install on Windows leaves skills broken.
- Likelihood: Low for primary developer; possible for contributors.
- Mitigation: CI runs on ubuntu only; provide `scripts/dereference-skills.sh` for Windows; document in CONTRIBUTING.
- Status: Open.

## Closed Risks

No closed risks recorded yet.
