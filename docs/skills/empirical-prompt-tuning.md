# empirical-prompt-tuning

Iteratively improve a skill or prompt by having a fresh subagent execute it against fixed scenarios, scoring two-sided (executor self-report + a frozen requirements checklist), and looping until improvements plateau.

## When to use

- After authoring or substantially revising a skill, slash command, subagent prompt, or CLAUDE.md addition.
- Before promoting a skill from draft to published.
- When a user reports unexpected skill behavior and you suspect instruction-side ambiguity.

## When not to use

- One-off throwaway prompts.
- Trivial wording changes.
- Personal taste disagreements (the method scores against frozen requirements, not preferences).

## Loop

1. Description / body consistency check (no dispatch).
2. Freeze 2–3 scenarios with `[critical]`-tagged requirements in `evals/<skill>/scenarios.yaml`.
3. Dispatch a **fresh** subagent per scenario via the `Task` tool.
4. Score two-sided: executor self-report (phase-tagged) + instruction-side metrics (pass/fail, accuracy, steps, duration, retries).
5. Apply the minimum fix; consult `evals/<skill>/ledger.md` first for recurring patterns.
6. Re-run with a **new** subagent.
7. Stop when two consecutive iterations plateau (three for high-importance skills).
8. Append a passing entry to `evals/<skill>/ledger.md`.

## Bookkeeping helpers

```sh
bash scripts/eval-skill.sh init <skill>      # scaffold evals/<skill>/
bash scripts/eval-skill.sh new-run <skill>   # create timestamped run note
bash scripts/eval-skill.sh status [<skill>]  # show iteration / last ledger entry
```

The full flow lives in [Skill Evaluation](../skill-evaluation.md). The CI quality gate (`eval-quality-gate.yml`) verifies every modified skill has a recent passing ledger entry.

## Attribution

Method from [mizchi/skills/empirical-prompt-tuning](https://github.com/mizchi/skills/tree/main/empirical-prompt-tuning). For the upstream skill verbatim:

```sh
apm install -g mizchi/skills/empirical-prompt-tuning
```

## Install

```sh
gh skill install s-hiraoku/claude-harnesses empirical-prompt-tuning --scope project
# or
npx skills add s-hiraoku/claude-harnesses --skill empirical-prompt-tuning
```
