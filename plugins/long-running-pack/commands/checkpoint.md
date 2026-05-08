---
description: Append a timestamped checkpoint with branch, commit, and short status to ledger/current.md.
argument-hint: ""
---

Run `bash scripts/checkpoint.sh` from the repo root. If the script is missing, fall back to inline equivalent: write a `### <UTC timestamp>` block with `Branch`, `Latest commit`, and `Short status` to `ledger/current.md`.

Then briefly state what is being checkpointed (one sentence).
