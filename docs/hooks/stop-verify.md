# stop-verify

Stop hook that runs `scripts/verify.sh` and blocks Stop on failure.

## Trigger

- Event: `Stop`

## What it does

1. Reentrancy guard: if `stop_hook_active` is `true` in the stdin envelope, exit 0 immediately (Claude is already inside a previously-blocked Stop, let it finish — this is critical to avoid infinite loops).
2. Find the repo root via `git rev-parse --show-toplevel`.
3. If `scripts/verify.sh` exists and is executable, run it.
4. On success, allow the stop. On failure, exit 2 to keep the session going so Claude can address it.

## Exit codes

- `0` — allow stop
- `2` — block stop (Claude continues working)

## Kill switches

- `CLAUDE_HARNESSES_DISABLE=1`

## Notes

The reentrancy guard is the most important property of this hook. Without it, a project that never produces evidence of fixing the verification failure would loop forever.

Pack: [verification-pack](../packs/verification-pack.md)
