# session-end-summary

SessionEnd hook that appends a brief end-of-session marker to the ledger.

## Trigger

- Event: `SessionEnd`

## What it does

When `ledger/current.md` exists at the repo root, append:

```
### <UTC timestamp> session end

- Session ended.
```

This gives the next session a clear pause point to resume from.

## Exit codes

Always `0`.

## Kill switches

- `CLAUDE_HARNESSES_DISABLE=1`

## Notes

Intentionally minimal; if you need richer per-session summaries, replace this with a hook that pulls duration / tool-call count from the cost ledger.

Pack: [long-running-pack](../packs/long-running-pack.md)
