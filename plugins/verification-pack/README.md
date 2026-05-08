# verification-pack

Tight verification feedback loop wired into Claude Code's hook lifecycle.

## Components

| Hook | Event | Purpose |
|---|---|---|
| `format-on-edit` | PostToolUse Edit/Write/MultiEdit | Run prettier/ruff/gofmt/rustfmt on the changed file. |
| `typecheck-on-edit` | PostToolUse Edit/Write | Run `tsc --noEmit` / `mypy` scoped to the changed file. |
| `test-on-edit` | PostToolUse Edit/Write | Run only the test file related to the changed file. |
| `stop-verify` | Stop | Block premature stops by running `scripts/verify.sh`; honors `stop_hook_active` to avoid infinite loops. |

| Command | Effect |
|---|---|
| `/verify` | Run the project's `scripts/verify.sh` (or the bundled fallback). |

## Install

```sh
claude /plugin install verification-pack@claude-harnesses
```

## Kill switch

`CLAUDE_HARNESSES_DISABLE=1` short-circuits every hook in this pack.
