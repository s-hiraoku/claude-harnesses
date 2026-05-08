# tdd

Drive development with Red-Green-Refactor using isolated test-writer, implementer, and refactorer subagents so tests reflect intent rather than anticipated implementation.

## Workflow

1. **Specify**: restate the desired behavior in 1–2 sentences and identify the testing framework.
2. **Red — `tdd-test-writer` subagent**: spec only, no implementation. Returns failing test path + failure output.
3. **Green — `tdd-implementer` subagent**: failing test only, no spec or earlier drafts. Smallest implementation that turns it green.
4. **Refactor — `tdd-refactorer` subagent**: post-Green code only. Improve clarity without changing behavior. Tests must stay green.
5. Loop for each behavior.

## Threat model

Context isolation is honor system: each subagent's prompt forbids reading certain inputs, and `tools` fields keep the surface narrow. The parent agent must honor the boundary; this is not a sandbox.

## Install

```sh
gh skill install s-hiraoku/claude-harnesses tdd --scope project
```

Part of `tdd-pack`. Slash command: `/tdd <behavior spec>`.
