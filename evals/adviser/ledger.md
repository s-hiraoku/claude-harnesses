# `adviser` failure-pattern ledger

Append one line per iteration. Newest at the bottom.

Format: `- YYYY-MM-DD: iter N, P/Q scenarios pass, accuracy R%, <plateau? blocker? note>`

## Failure patterns observed

(One entry per recurring `General Fix Rule`. Don't add a new entry for a recurrence — move the existing fix to a more prominent position first and note it here.)

| First seen | General Fix Rule | Where the fix lives | Recurrences |
|---|---|---|---|
| 2026-07-10 | Name material ambiguity as an escalation trigger. | Workflow step 7 | 0 |
| 2026-07-10 | Never claim a consultation that did not return. | Fallback | 0 |
| 2026-07-10 | Distinguish prompt-enforced reviewer behavior from a tool-permission boundary. | Overview, Workflow step 4, Prompt Contract | 0 |

## Iteration log

- 2026-07-10: iter 1, 2/2 scenarios pass, accuracy 100%, two wording ambiguities fixed; no critical failures
- 2026-07-10: review hardening pass, replaced unenforced “read-only” claims with an explicit instruction-level review-only role
