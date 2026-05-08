# cost-ceiling-guard

PreToolUse hook that caps cumulative tool calls per 24h window to prevent runaway loops.

## Trigger

- Event: `PreToolUse`

## What it does

Persists a rolling 24h counter at `~/.claude-harnesses/cost-ledger.json`. Increments on every PreToolUse. Past the ceiling (default 5000), exits 2 to deny the next tool call.

To stay cheap on the hot path, the ledger is rewritten only:

- on the first call,
- every 10th call,
- when the count is within 100 of the ceiling.

## Exit codes

- `0` — allow
- `2` — block (cost ceiling exceeded)

## Tunables

| Env var | Default | Effect |
|---|---|---|
| `CLAUDE_HARNESSES_DISABLE` | unset | `=1` disables the hook |
| `CLAUDE_HARNESSES_COST_CEILING` | `5000` | Calls per 24h before forced stop |
| `CLAUDE_HARNESSES_COST_PATH` | `~/.claude-harnesses/cost-ledger.json` | Override ledger path |

## Reset

```sh
rm ~/.claude-harnesses/cost-ledger.json
```

Pack: [long-running-pack](../packs/long-running-pack.md)
