# `no-slop` failure-pattern ledger

Append one line per iteration. Newest at the bottom.

Format: `- YYYY-MM-DD: iter N, P/Q scenarios pass, accuracy R%, <plateau? blocker? note>`

## Failure patterns observed

| First seen | General Fix Rule | Where the fix lives | Recurrences |
|---|---|---|---|
| 2026-07-23 | Preserve unsupported source claims with visible uncertainty; never invent support. | `skills/no-slop/SKILL.md`, rule 2 | 0 |
| 2026-07-23 | Verify every protected operational information type, not only generic facts. | `skills/no-slop/SKILL.md`, preservation pass | 0 |

## Iteration log

- 2026-07-23: iter 2, 3/3 scenarios pass, accuracy 100%, plateau confirmed (2 consecutive); unsupported-claim and operational-preservation ambiguity resolved
