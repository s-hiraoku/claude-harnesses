---
description: Drive a Red-Green-Refactor cycle for a behavior using isolated tdd-test-writer, tdd-implementer, and tdd-refactorer subagents.
argument-hint: "<short behavior spec>"
---

Run the `tdd` skill for behavior: $ARGUMENTS

Sequence:

1. **Red**: Spawn `tdd-test-writer` with the spec only. Receive the failing-test path and failure output.
2. **Green**: Spawn `tdd-implementer` with only the failing-test path. Receive the diff and passing status.
3. **Refactor**: Spawn `tdd-refactorer` with the post-Green file path. Confirm tests still pass.

Do not pass the spec to the implementer. Do not pass the implementation to the test-writer. Each subagent runs in an isolated context window.
