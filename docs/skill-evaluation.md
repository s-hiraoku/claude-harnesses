# Skill Evaluation

`claude-harnesses` keeps skill quality high by treating every skill as a prompt that must be **empirically tuned** before release. The flow is borrowed from [mizchi/skills/empirical-prompt-tuning](https://github.com/mizchi/skills/tree/main/empirical-prompt-tuning); the canonical method lives in our own [`empirical-prompt-tuning` skill](skills/empirical-prompt-tuning.md).

## Why

The author of a skill cannot judge its quality. Re-reading your own draft from "the same head" cannot detect the ambiguities that will trip up a fresh agent. The only reliable test is to dispatch a bias-free executor, score against a frozen requirements checklist, and iterate until improvements plateau.

## Flow

```
authored / revised SKILL.md
        │
        ▼
 evals/<skill>/scenarios.yaml   ← freeze 2–3 scenarios + checklists
        │
        ▼
 dispatch fresh subagent via Task tool, one per scenario
        │
        ▼
 fill evals/<skill>/runs/<timestamp>.md   ← two-sided scoring
        │
        ▼
 minimum fix to SKILL.md, one theme per iteration
        │
        ▼
 loop with a NEW subagent until 2 consecutive plateau iterations
        │
        ▼
 append passing entry to evals/<skill>/ledger.md
        │
        ▼
 PR's eval-quality-gate.yml verifies the ledger entry
```

## Step-by-step

### 1. Scaffold

```sh
bash scripts/eval-skill.sh init <skill-name>
```

Creates `evals/<skill>/scenarios.yaml`, `evals/<skill>/runs/`, and `evals/<skill>/ledger.md` from `evals/_template/`.

### 2. Define scenarios

Edit `evals/<skill>/scenarios.yaml`. Pick **2–3** scenarios (1 typical + 1 edge minimum). For each scenario, list **3–7 requirements**, with at least one tagged `[critical]`. Once a run has been recorded, **do not edit checklists retroactively** — that turns the eval into a vibes check.

### 3. Start a run

```sh
bash scripts/eval-skill.sh new-run <skill-name>
```

Creates a timestamped run file under `evals/<skill>/runs/`.

### 4. Dispatch fresh subagents

Inside Claude Code, for each scenario, dispatch a `general-purpose` subagent with **only** the scenario prompt. Do not paste the SKILL.md, do not summarize it. Multiple scenarios go in a single message for parallelism.

### 5. Score two-sided

Fill the run file with:

- **Executor self-report**: phase-tagged unclear points, discretionary fill-ins.
- **Instruction-side metrics**: pass/fail (only if all `[critical]` items pass), accuracy %, tool-use steps (`tool_uses`), duration ms (`duration_ms`), retry count.
- **Structured reflection**: `Issue / Cause / General Fix Rule` per unclear point.

### 6. Apply the minimum fix

Before editing the SKILL.md, state which checklist item the fix is meant to satisfy. Consult the ledger first — recurring patterns mean the existing fix is in the wrong place.

### 7. Re-run

Always with a **new** subagent. Old subagents have already learned the prior text.

### 8. Stop conditions

- Two consecutive iterations with zero new unclear points,
- AND accuracy / step / duration improvements below 5%.

For high-importance skills, require three consecutive plateau iterations.

### 9. Record and gate

Append a one-line entry to `evals/<skill>/ledger.md`:

```
- 2026-05-09: iter 3, 3/3 scenarios pass, accuracy 92%, plateau confirmed
```

The CI workflow `eval-quality-gate.yml` reads this ledger on every PR that touches `skills/<name>/SKILL.md`. PRs without a recent passing ledger entry fail the gate. Trivial changes can opt out with `[skip-eval]` in the PR description.

## CI configuration

`.github/workflows/eval-quality-gate.yml` runs `scripts/check-eval-coverage.py` against `origin/<base ref>`. The script:

1. Lists `skills/<name>/SKILL.md` files changed in the PR.
2. For each, requires `evals/<name>/ledger.md` to contain a dated entry within the last 14 days **and** mention `pass` / `plateau` / `converged`.
3. Bypasses with `[skip-eval]` in the PR body.

## Status check

```sh
bash scripts/eval-skill.sh status            # all skills
bash scripts/eval-skill.sh status review     # one skill
```

## Anti-patterns

- **Re-reading your own draft and "deciding it's clear."** Dispatch a fresh subagent.
- **Editing the requirements checklist after seeing the run.** Defeats the metric.
- **Reusing the same subagent across iterations.** It has learned the prior text.
- **Adding new ledger entries for recurring patterns.** Move the existing fix to a more prominent position before recording another instance.

## Attribution

The method comes from [mizchi/skills/empirical-prompt-tuning](https://github.com/mizchi/skills/tree/main/empirical-prompt-tuning). To use the upstream skill verbatim instead of our adaptation:

```sh
apm install -g mizchi/skills/empirical-prompt-tuning
```
