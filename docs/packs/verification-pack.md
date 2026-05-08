# verification-pack

Tight verification feedback wired into every edit and Stop event.

| Hook | Event | Purpose |
|---|---|---|
| `format-on-edit` | PostToolUse Edit/Write/MultiEdit | prettier / ruff / gofmt / rustfmt on the changed file |
| `typecheck-on-edit` | PostToolUse Edit/Write | `tsc --noEmit` / `mypy` scoped to the changed file |
| `test-on-edit` | PostToolUse Edit/Write | only the test file related to the changed file |
| `stop-verify` | Stop | block premature stops; honors `stop_hook_active` to avoid loops |

Slash command: `/verify` runs `bash scripts/verify.sh`.

Install: `claude /plugin install verification-pack@claude-harnesses`
