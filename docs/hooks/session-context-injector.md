# session-context-injector

SessionStart hook that injects git status and ledger head as additional context.

## Trigger

- Event: `SessionStart`

## What it does

Emits a markdown block:

- Current branch (`git branch --show-current`)
- Working-tree changes (first 10 lines of `git status --short`)
- Head of `ledger/current.md` (lines 2..31) when the file exists

Claude Code captures this as additional context for the new session.

## Exit codes

Always `0`.

## Kill switches

- `CLAUDE_HARNESSES_DISABLE=1`

## Notes

Output is bounded so it never exceeds Claude Code's 10,000-character context-injection limit on small-to-medium repos. Long working-tree status is truncated at 10 lines.

Pack: [long-running-pack](../packs/long-running-pack.md)
