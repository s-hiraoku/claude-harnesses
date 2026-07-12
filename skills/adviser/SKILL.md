---
name: adviser
description: Consult a fresh, review-only Claude subagent as a fallback for environments where the native Advisor tool is unavailable. Use when the user asks for an adviser, advisor, second opinion, stronger-model review, or /advisor-like behavior; before committing to a consequential multi-step approach; when work is stuck or changing direction; and before declaring substantial work complete.
---

# Adviser

Use a fresh `Task` subagent as an independent strategic reviewer when Claude Code's native Advisor tool is unavailable. Prefer `model: opus`; if Opus is unavailable, use the strongest permitted model and disclose the downgrade. “Fresh” means a newly spawned reviewer that has taken no prior task actions. “Review-only” is an instruction-level role, not a sandbox boundary, unless the runtime separately restricts the subagent's tools. The main agent remains the executor and owns all tools, edits, decisions, and final reporting.

This fallback emulates native Advisor's decision pattern, not its server implementation. It cannot guarantee complete transcript delivery, same-turn sub-inference, native model-pair validation, usage accounting, prompt-cache behavior, or Advisor UI. Report the reviewer as `stronger`, `same-tier`, or `unknown` only when the runtime exposes enough evidence; selecting Opus does not by itself prove an upgrade over the main model. Unknown model strength does not make the reviewer unavailable: if a Task subagent returns advice, count the consultation and label its capability `unknown`.

## Workflow

1. Check for native Advisor availability. If the native `advisor` tool is active, use it instead of this fallback. Do not run both for ceremony.
2. Orient before consulting. Gather the minimum repository evidence needed for a useful review. File discovery, source retrieval, and current-state inspection are orientation; editing, settling an interpretation, and declaring completion are substantive work.
3. Decide whether consultation adds value at the current decision point. Favor long multi-step work, consequential or ambiguous choices, recurring failures, and independent completion checks. Skip short mechanical tasks and work where every step genuinely requires the strongest available main model.
4. Build a consultation packet containing the user goal, relevant constraints, inspected facts and tool results, assumptions, proposed decision, unresolved questions, verification plan, and—at completion—changed artifacts, diff summary, test results, and known risks. Never include secrets or irrelevant transcript content. Do not claim the reviewer receives the complete parent transcript.
5. Spawn one fresh `general-purpose` Task subagent with `model: opus` and the prompt contract below. Instruct it to return review text only: no file edits, commands, delegation, or task ownership. If the runtime supports per-agent tool restrictions, disable mutating tools as defense in depth. If Opus is rejected or unavailable, retry once with the strongest permitted model and record the downgrade. Continue with capability `unknown` when model metadata is absent; use the self-review fallback only when no Task subagent can launch and return advice.
6. Weigh the advice. Adopt supported recommendations, but prefer repository evidence, primary sources, and empirical results over unsupported conflicting advice. Record material approach changes in the normal plan or commentary.
7. Reconcile material conflicts. When evidence contradicts the adviser, continue the same Task conversation if the runtime supports follow-ups so it can defend or revise its exact claim. Otherwise spawn one fresh adviser with the original advice and conflicting evidence. Do not silently switch directions or loop over minor disagreements.
8. Reconsult when material ambiguity blocks a decision, the same failure recurs, the approach stops converging, or a materially different approach is under consideration.
9. Before declaring substantial work complete, save the deliverable and run relevant verification. Consult again when an independent completion check is valuable. Fix actionable findings and rerun only checks affected by those fixes.

Typical high-value checkpoints are after orientation but before choosing an approach, and after verification but before completion. These are model-driven defaults, not a fixed quota or mandatory two-call rule. Honor an explicit user request to consult before continuing or to skip Adviser for the task.

## Prompt Contract

Use this bounded Task prompt, followed by the consultation packet:

```text
Act as the Adviser: an independent, review-only strategic reviewer. Return review text only. Do not edit files, run commands, delegate, or take over execution. Review only the supplied consultation packet. Identify incorrect assumptions, missed constraints, evidence conflicts, likely failure modes, and the best next approach. Distinguish evidence-backed findings from uncertainty. Be concise. End with exactly four sections: Recommendation, Critical risks, Evidence conflicts, Completion checks.
```

At the completion gate, ask whether the result is ready to report complete and request only actionable gaps.

## Fallback

If no Task subagent can be launched, perform a clearly separated second-pass review using the same prompt contract. State that independent review and model escalation were unavailable. Never claim that the native Advisor tool or any fallback reviewer ran unless that consultation actually returned a response.

## Final Report

Include whether native Advisor was unavailable, the number and timing of fallback consultations, capability class (`stronger`, `same-tier`, or `unknown`), model used or downgrade, material advice followed or rejected, context-delivery limitations, verification status and checks rerun after adviser-driven changes, and residual risk. Do not expose hidden reasoning or paste the full consultation transcript.
