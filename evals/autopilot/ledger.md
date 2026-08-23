# `autopilot` failure-pattern ledger

Append one line per iteration. Newest at the bottom.

Format: `- YYYY-MM-DD: iter N, P/Q scenarios pass, accuracy R%, <plateau? blocker? note>`

## Failure patterns observed

| First seen | General Fix Rule | Where the fix lives | Recurrences |
|---|---|---|---|

## Iteration log

- 2026-08-23: iter 0 structural checks passed; empirical scenario execution pending.
- 2026-08-23: iter 1, 2/2 fresh-agent scenarios pass, accuracy 100%, explicit-only routing, fork-head authority, PR Guardian delegation, and no-merge boundaries all satisfied.
- 2026-08-23: iter 2, 2/2 fresh hold-out scenarios pass, accuracy 100%, no new unclear points and zero accuracy delta; converged against committed Skill `bf1d94e`.
