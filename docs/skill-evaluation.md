# Skill Evaluation

Every skill in this repository is treated as a prompt that must be **empirically tuned** before release. This page is the practical how-to. The method itself lives in the [`empirical-prompt-tuning`](skills/empirical-prompt-tuning.md) skill, adapted from [mizchi/skills/empirical-prompt-tuning](https://github.com/mizchi/skills/tree/main/empirical-prompt-tuning).

## Why bother

The author of a skill cannot judge its quality. Re-reading your own draft from "the same head" cannot detect the ambiguities that will trip up a fresh agent. The only reliable test is to dispatch a bias-free executor, score against a frozen requirements checklist, and iterate until improvements plateau.

## When to run an evaluation

- After authoring a new skill.
- After substantially revising a skill's body or `description`.
- Before promoting a skill from draft to published (i.e. before merging to main).
- When a user reports unexpected behavior and you suspect instruction-side ambiguity.

Skip evaluation only for typo / link / formatting fixes — and use `[skip-eval]` in the PR description so CI knows.

## End-to-end example: evaluating the `review` skill

Concrete walkthrough of one full iteration. Every other skill follows the same shape.

### Step 1 — scaffold the eval directory

```sh
bash scripts/eval-skill.sh init review
```

Creates:

```
evals/review/
├── scenarios.yaml      # to be filled
├── runs/               # timestamped run notes will land here
└── ledger.md           # dated iteration summaries
```

### Step 2 — write `evals/review/scenarios.yaml`

Pick **2–3 scenarios** (1 typical + 1 edge minimum). For each, list **3–7 requirements**, with **at least one tagged `[critical]`**. Once a run records against this file, **do not edit checklists retroactively** — that turns the eval into a vibes check.

```yaml
skill: review

scenarios:
  - id: typical-pr
    kind: typical
    prompt: |
      Review the current branch as if it were a PR adding rate limiting
      to src/api/auth.ts. The branch adds a new middleware, modifies
      src/api/server.ts to wire it in, and adds 2 tests. Produce a
      severity-ranked review.
    requirements:
      - text: Findings are listed in severity order (Critical → Info).
        critical: true
      - text: Each finding cites a file:line.
        critical: true
      - text: A one-line verdict (Ready to Merge / Needs Attention / Needs Work) is included.
        critical: true
      - text: Style nits are not raised unless they obscure correctness.
        critical: false

  - id: empty-diff
    kind: edge
    prompt: |
      Review the current branch. The branch has zero commits relative to main.
    requirements:
      - text: The skill recognizes the empty diff and reports it explicitly.
        critical: true
      - text: No invented findings.
        critical: true
```

### Step 3 — create a run note

```sh
bash scripts/eval-skill.sh new-run review
```

This creates `evals/review/runs/<timestamp>.md` from the template, pre-filled with the current skill commit hash and iteration number.

### Step 4 — ask Claude to run the evaluation

Open Claude Code in the repo and say:

> Use the `empirical-prompt-tuning` skill to evaluate the `review` skill for one iteration. Read `evals/review/scenarios.yaml`, dispatch one fresh subagent per scenario via the Task tool (in parallel), and fill in `evals/review/runs/<the new file>.md`. Do not paste the skill body to the subagents — they must read it cold.

Claude will:

1. Read `scenarios.yaml`.
2. Spawn one `general-purpose` subagent **per scenario** in a single message (parallel).
3. Pass each subagent **only** the scenario `prompt` field. Not the SKILL.md content.
4. Collect the subagents' returns plus `tool_uses` / `duration_ms` from the Task usage meta.
5. Score two-sided into the run file:
   - **Executor self-report** (phase-tagged: Understanding / Planning / Execution / Formatting)
   - **Instruction-side metrics**: pass/fail (only if all `[critical]` items pass), accuracy %, tool steps, duration ms, retry count
   - **Structured reflection** per unclear point: `Issue / Cause / General Fix Rule`

### Step 5 — apply the minimum fix

Read the filled-in run file. Before editing the SKILL.md, write down **which checklist item the fix is meant to satisfy**. Then make the smallest change to `skills/review/SKILL.md` that addresses it. One theme per iteration; unrelated cleanups go to the next iteration.

Consult `evals/review/ledger.md` first. If the same `General Fix Rule` keeps appearing, the existing fix is in the wrong place — move it before adding a new ledger entry.

### Step 6 — re-run with a NEW subagent

```sh
bash scripts/eval-skill.sh new-run review
```

Then ask Claude again, the same prompt as Step 4. **Do not reuse the previous subagent** — it has already read the prior text and the eval becomes a reading-comprehension test of the previous version.

### Step 7 — converge

Stop when:

- **Two consecutive iterations** produce zero new unclear points, AND
- Accuracy / step count / duration improvements drop below 5%.

For high-importance skills (e.g. anything in `safety-pack` or `verification-pack`), require **three** consecutive plateau iterations.

### Step 8 — record in the ledger

Append one line to `evals/review/ledger.md`:

```
- 2026-05-09: iter 3, 2/2 scenarios pass, accuracy 100%, plateau confirmed (2 consecutive)
```

The CI gate looks for an entry like this.

## CI quality gate

Every PR that modifies `skills/<name>/SKILL.md` is checked by `.github/workflows/eval-quality-gate.yml`. The gate runs `scripts/check-eval-coverage.py`, which:

1. Lists changed `SKILL.md` files via `git diff` against the base ref.
2. For each, requires `evals/<name>/ledger.md` to contain a dated entry **within the last 14 days** that mentions `pass`, `plateau`, or `converged`.
3. Bypasses cleanly when `[skip-eval]` appears in the PR body (use only for trivial changes — typos, link fixes — with a one-line justification).

If the gate fails, run another iteration, append a fresh ledger entry, and push.

## Status overview

```sh
bash scripts/eval-skill.sh status            # all skills with eval dirs
bash scripts/eval-skill.sh status review     # one specific skill
```

Output shows the run count and the most recent dated ledger entry.

## Prompt template for Claude

Drop this into a Claude Code session whenever you start an iteration. Replace `<skill>` with the skill under evaluation.

> Use the `empirical-prompt-tuning` skill to run iteration N of evaluating `<skill>`.
> 1. Read `evals/<skill>/scenarios.yaml`.
> 2. Use `bash scripts/eval-skill.sh new-run <skill>` to create the run file (or use the latest empty one if I already created it).
> 3. Dispatch one `general-purpose` subagent **per scenario in parallel** via the Task tool. Pass each subagent ONLY the scenario `prompt` field — do not paste or summarize the SKILL.md.
> 4. Capture from each return: full subagent response, `tool_uses`, `duration_ms`.
> 5. Fill the run file with two-sided scoring (executor self-report phase-tagged, instruction-side metrics, structured reflection per unclear point).
> 6. Propose the minimum fix to `skills/<skill>/SKILL.md`, citing the checklist item it addresses. Do not apply yet.
> 7. End with the proposed diff and ask me to approve before writing.

## Anti-patterns

- **Re-reading your own draft and "deciding it's clear."** Your head has the missing context already. Dispatch a fresh subagent.
- **Editing the requirements checklist after seeing the run.** Converts the eval to a vibes check.
- **Reusing the same subagent across iterations.** It has learned the prior text.
- **Adding a new ledger entry for a recurring class of failure.** That just multiplies notes. Move the existing fix to a more prominent position first.
- **Pasting the SKILL.md into the subagent's prompt.** It must read the skill the way a future user would — cold.

## Attribution

The method comes from [mizchi/skills/empirical-prompt-tuning](https://github.com/mizchi/skills/tree/main/empirical-prompt-tuning). To use the upstream skill verbatim instead of our adaptation:

```sh
apm install -g mizchi/skills/empirical-prompt-tuning
```
