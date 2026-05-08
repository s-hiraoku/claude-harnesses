---
description: Run the project's verification script (lint, typecheck, test, build) and report the result.
argument-hint: ""
---

Run `bash scripts/verify.sh` from the repo root. If it exits non-zero, summarize the failing step and propose the smallest fix.

If `scripts/verify.sh` is absent, fall back to `${CLAUDE_PLUGIN_ROOT}/scripts/verify.sh` from this plugin, which detects npm / pyproject / mkdocs and runs the equivalent commands.
