# Evaluation run

- Skill: `<skill-name>`
- Skill commit: `<git rev-parse HEAD of skills/<skill-name>>`
- Iteration: `N`
- Started: `<UTC ISO timestamp>`
- Operator: `<who ran this>`

## Subagent dispatch

Type: `general-purpose`
Model: `<model id>`
Scenarios run: `<count>`

## Per-scenario results

### Scenario `typical`

- Pass / fail: ○ / × (all `[critical]` items satisfied?)
- Accuracy: `M / N = X%` (full=1, partial=0.5, fail=0)
- Tool uses: `<from usage meta>`
- Duration ms: `<from usage meta>`
- Retry count: `<from subagent self-report>`

#### Requirements checklist

| Item | Critical | Result | Note |
|---|---|---|---|
| ... | ✓ / – | ○ / × / partial | |

#### Executor self-report

| Phase | Unclear point | Discretionary fill-in |
|---|---|---|
| Understanding | | |
| Planning | | |
| Execution | | |
| Formatting | | |

#### Structured reflection

| Issue | Cause | General Fix Rule |
|---|---|---|
| | | |

### Scenario `edge`

(same shape as above)

## Aggregate

- Scenarios pass: `X / Y`
- Mean accuracy: `Z%`
- Median tool uses: `K`
- Median duration ms: `L`

## Diff applied this iteration

(`git diff` summary against the previous iteration's skill content)

## Convergence check

- Iterations with zero new unclear points so far: `N consecutive`
- Δaccuracy vs. previous iteration: `+/− %`
- Δstep count vs. previous iteration: `+/− steps`
- Decision: continue / converged
