---
name: kaizen-loop
description: "Run a continuous product improvement loop: evaluate a product or codebase, present prioritized recommendations for approval, then implement only approved improvements through verification and PR follow-up."
---

# Kaizen Loop

Use this workflow when the task starts with product evaluation rather than a known implementation request. First evaluate the product as a user, engineer, and maintainer; then present concrete improvement candidates; after the user approves items, execute them with `implement-to-merge-ready` and repeat the evaluation loop.

## Workflow

1. Establish evaluation scope.
   - Identify the product, target user, primary workflows, success criteria, repository, branch, and deployment or local run path.
   - Read local instructions such as `AGENTS.md` and `CLAUDE.md`.
   - Inspect `git status` and preserve unrelated user changes.
   - Ask only when the evaluation target or approval boundary is unclear.
2. Set an evaluation goal.
   - Use goal tracking for product-wide evaluation or work expected to continue into implementation and PR follow-up.
   - Include evaluation, recommendation, approval gate, approved implementation, verification, PR creation, and merge-readiness follow-up.
3. Build product understanding.
   - Read product docs, routes, screens, tests, analytics assumptions, configuration, and recent changes.
   - Run the app locally when practical.
   - For frontend products, inspect key screens in a real browser across representative desktop and mobile viewports.
   - For APIs or libraries, inspect public interfaces, examples, error behavior, docs, and test coverage.
4. Evaluate relevant dimensions.
   - User value, UX/UI, correctness, performance, reliability, engineering quality, security, privacy, docs, and release risk.
   - Label inferences clearly when evidence is indirect.
5. Produce an evaluation report before editing.
   - Lead with highest-impact findings.
   - For each candidate include problem, impact, evidence, likely fix direction, estimated scope, risk, and suggested verification.
   - Separate must-fix defects from product improvements and speculative ideas.
6. Ask for approval to proceed.
   - Present a short prioritized list of recommended improvements.
   - Treat silence or ambiguity as no approval for implementation.
   - If multiple items are approved, group them into the smallest coherent PRs.
7. Implement approved improvements only.
   - Use `implement-to-merge-ready` for each approved change or coherent group.
   - Use `ui-imagegen-director` before coding when UI visual direction matters.
   - Do not opportunistically fix unapproved items.
8. Review, open PRs, and bring them toward merge-ready.
   - Self-review against the approved scope and evaluation evidence.
   - Open regular ready-for-review PRs by default.
   - Monitor CI and review feedback when practical.
9. Re-evaluate after approved changes.
   - Confirm the approved problems were resolved.
   - Identify newly visible opportunities and wait for approval before repeating.

## Recommendation Format

```text
Evaluation summary:
- <one short product-level assessment>

Recommended improvements:
1. <title> [impact: high|medium|low, scope: small|medium|large]
   Problem: <what is wrong>
   Evidence: <what was observed>
   Fix direction: <what should change>
   Verification: <how to know it worked>

Please tell me which item numbers to implement.
```

## Guardrails

- Evaluation may inspect broadly, but implementation must stay within approved scope.
- Do not fabricate user research, metrics, analytics, security findings, or benchmark results.
- Prefer concrete, verifiable improvements over broad redesign advice.
- Do not merge PRs unless the user explicitly asks and repository policy permits it.

## Final Report

Include evaluation scope and evidence, approved improvements implemented, PR URLs/branches/status, verification before and after implementation, resolved issues, remaining recommendations, and goal status when used.
