---
name: empirical-prompt-tuning
description: Iteratively improve a skill or prompt by having a fresh subagent execute it against fixed scenarios, scoring two-sided (executor self-report + a pre-frozen requirements checklist), and looping until improvements plateau. Use after authoring or revising any skill, slash command, or CLAUDE.md addition.
---

# Empirical Prompt Tuning

The author of a prompt cannot judge its quality. Whoever wrote the text already understands the implicit context, so re-reading it from "the same head" cannot detect ambiguity. The only reliable way to find ambiguity is to **dispatch a bias-free executor, score the run two-sidedly, and iterate until improvements stop**.

This skill is a method, not a tool. It runs inside Claude Code with the `Task` tool to spawn fresh subagents. The repository's `scripts/eval-skill.sh` and `evals/` directory mechanize the bookkeeping; this SKILL.md is the workflow.

Inspired by [mizchi/skills/empirical-prompt-tuning](https://github.com/mizchi/skills/tree/main/empirical-prompt-tuning). The original is the canonical reference; install it via `apm install -g mizchi/skills/empirical-prompt-tuning` if you want the upstream version verbatim.

## When to use

- Right after creating or substantially revising a skill, slash command, subagent prompt, or CLAUDE.md addition in this repo.
- When a skill is about to be promoted from "draft" to "published" (i.e. before merge to main).
- When a user reports the skill behaved unexpectedly and you suspect instruction-side ambiguity rather than model failure.

When **not** to use:

- One-off throwaway prompts.
- Trivial wording changes (typos, link fixes).
- When you only want to check personal taste — this method scores against frozen requirements, not preferences.

## Workflow

### 0. Description / body consistency check

Before spawning anything, read the SKILL.md frontmatter `description` and confirm the body actually covers what the description claims. If the description says "blocks A, B, C" but the body only describes A, fix one or the other first. Skipping this lets a subagent silently reinterpret the body to match the description, producing a false positive.

### 1. Freeze the evaluation harness

Create `evals/<skill-name>/scenarios.yaml` with 2–3 realistic scenarios (1 typical + 1 edge), each with a **requirements checklist** of 3–7 items. Tag at least one item per scenario as `[critical]`. Once a run is recorded, you may not edit checklists retroactively — that defeats the metric.

Use `evals/_template/scenarios.yaml` as the starting point. Run:

```sh
bash scripts/eval-skill.sh init <skill-name>
```

to scaffold the directory.

### 2. Bias-free dispatch

For each scenario, spawn a **fresh** subagent via the `Task` tool with the `general-purpose` (or skill-appropriate) type. Pass the scenario prompt only — do not paste the SKILL.md, do not summarize it, do not hint at the answer. The subagent must read the skill cold, the same way a future user would.

Example (one tool call per scenario; multiple scenarios go in a single message for parallelism):

```
Task(
  subagent_type: "general-purpose",
  description: "Evaluate <skill-name>",
  prompt: "<scenario.prompt from scenarios.yaml>"
)
```

### 3. Two-sided scoring

For each subagent return, fill in `evals/<skill-name>/runs/<timestamp>.md` (template at `evals/_template/run.md`). Capture **both** sides:

- **Executor self-report**: unclear points, discretionary fill-ins, places where the skill's template did not fit. Tag each by the phase it surfaced in (Understanding / Planning / Execution / Formatting).
- **Instruction-side metrics**:
  - Pass / fail: success only if **all** `[critical]` items were satisfied.
  - Accuracy %: items satisfied / total (full = 1.0, partial = 0.5, fail = 0).
  - Tool-use steps: from the Task tool's usage meta `tool_uses`.
  - Duration ms: from the Task tool's usage meta `duration_ms`.
  - Retry count: how many times the subagent re-decided the same thing (from its self-report).

For each unclear point, record `Issue / Cause / General Fix Rule` so future runs can spot the same class of failure.

### 4. Apply the minimum fix

Edit the skill body to remove the unclear points found. One theme per iteration (related fixes OK; unrelated go to the next iteration). Before writing the fix, state in the run note **which checklist item this fix is meant to satisfy** — fixes inferred from vibes tend not to land.

Consult `evals/<skill-name>/ledger.md` first. If the same `General Fix Rule` keeps appearing, the existing fix is in the wrong location (too low in the document, too soft, ambiguous trigger) — move it before adding a new entry.

### 5. Loop

Re-run with a **new** subagent (never reuse — it has already learned the prior fix). Stop when:

- Two consecutive iterations produce zero new unclear points,
- AND accuracy / step / duration improvements fall below 5% relative to the previous iteration.

For high-importance skills (used by the safety/verification packs), require three consecutive plateau iterations.

### 6. Record

Append a one-line summary to `evals/<skill-name>/ledger.md`:

```
- 2026-05-09: iter 3, 3/3 scenarios pass, accuracy 92%, plateau confirmed (2 consecutive)
```

The CI quality gate (`.github/workflows/eval-quality-gate.yml`) reads this ledger to verify each modified skill has a recent passing entry.

## Quality gate (CI)

A skill PR that modifies `skills/<name>/SKILL.md` must include either:

1. A new entry in `evals/<name>/ledger.md` showing a passing run on the new content, OR
2. A `[skip-eval]` token in the PR description **with a one-line justification** (typo fix, doc-only, etc.).

The workflow `eval-quality-gate.yml` enforces this on PR.

## Anti-patterns

- **Re-reading your own draft and "deciding it's clear."** Your head already has the missing context. Dispatch a fresh subagent.
- **Editing the requirements checklist after seeing the run.** This converts the eval into a vibes check.
- **Reusing the same subagent across iterations.** It has learned the prior text; the eval becomes a reading-comprehension test of the previous version.
- **Adding a new ledger entry for a recurring class of failure.** That just multiplies notes. Move the existing fix to a more prominent position first.

## Final report template

When the loop converges, the final response should include:

- skill name and final commit hash
- iterations run, with per-iteration accuracy and step count
- the failure-pattern ledger entries that were resolved
- residual known limitations
- pointer to the latest run file
