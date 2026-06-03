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

- Risk: Skill symlinks from `plugins/*/skills/<name>` to `skills/<name>` (and `plugins/*/_shared`) become text files on Windows + Git without `core.symlinks=true`.
- Impact: Plugin install on Windows leaves skills broken and safety/verification/long-running hooks unable to import `_shared/envelope.py` / source `_shared/hook-prelude.sh`.
- Likelihood: Low for primary developer; possible for contributors.
- Mitigation: CI runs on ubuntu only; `scripts/validate-plugins.sh` + `tests/test_plugins.py` fail loud if any link is dangling. Note: `scripts/dereference-skills.sh` is referenced as a future mitigation but not yet implemented.
- Status: Open (link-resolution now CI-enforced 2026-06-04; Windows dereference helper still TODO).

## Closed Risks

No closed risks recorded yet.
