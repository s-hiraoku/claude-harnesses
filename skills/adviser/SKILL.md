---
name: adviser
description: Consult a fresh, review-only Claude subagent as a fallback for environments where the native Advisor tool is unavailable. Use when the user asks for an adviser, advisor, second opinion, stronger-model review, or /advisor-like behavior; before committing to a consequential multi-step approach; when work is stuck or changing direction; and before declaring substantial work complete.
---

# Adviser

Use a fresh `Task` subagent as an independent strategic reviewer when Claude Code's native Advisor tool is unavailable. Prefer `model: opus`; if Opus is unavailable, use the strongest permitted model and disclose the downgrade. “Fresh” means a newly spawned reviewer that has taken no prior task actions. “Review-only” is an instruction-level role, not a sandbox boundary, unless the runtime separately restricts the subagent's tools. The main agent remains the executor and owns all tools, edits, decisions, and final reporting.

## Workflow

1. Check for native Advisor availability. If the native `advisor` tool is active, use it instead of this fallback. Do not run both for ceremony.
2. Orient before consulting. Gather the minimum repository evidence needed for a useful review. File discovery, source retrieval, and current-state inspection are orientation; editing, settling an interpretation, and declaring completion are substantive work.
3. Before substantive work on a multi-step or consequential task, build a consultation brief containing the user goal, relevant constraints, evidence already inspected, assumptions, proposed approach, open decisions, risks, and verification plan. Never include secrets or irrelevant transcript content.
4. Spawn one fresh `general-purpose` Task subagent with `model: opus` and the prompt contract below. Instruct it to return review text only: no file edits, commands, delegation, or task ownership. If the runtime supports per-agent tool restrictions, disable mutating tools as defense in depth. If Opus is rejected or unavailable, retry once with the strongest permitted model and record the downgrade.
5. Weigh the advice. Adopt supported recommendations, but prefer repository evidence, primary sources, and empirical results over unsupported conflicting advice. Record material approach changes in the normal plan or commentary.
6. Reconcile conflicts. When evidence contradicts the adviser, continue the same Task conversation if the runtime supports follow-ups so it can defend or revise its exact claim. Otherwise spawn one fresh adviser with the original advice and conflicting evidence. Do not silently switch directions.
7. Reconsult when material ambiguity blocks a decision, the same failure recurs, the approach stops converging, or a materially different approach is under consideration.
8. Before declaring substantial work complete, save the deliverable and run relevant verification. Spawn a fresh completion adviser with the outcome, diff or artifact summary, verification evidence, and known risks. Fix actionable findings and rerun only checks affected by those fixes.

For work longer than a few steps, target two consultations: one after orientation and before choosing the approach, and one after verification and before completion. Skip ritual consultations for short reactive work whose next action is dictated by fresh tool output.

## Prompt Contract

Use this bounded Task prompt, followed by the consultation brief:

```text
Act as the Adviser: an independent, review-only strategic reviewer. Return review text only. Do not edit files, run commands, delegate, or take over execution. Review only the supplied consultation brief. Identify incorrect assumptions, missed constraints, likely failure modes, and the best next approach. Distinguish evidence-backed findings from uncertainty. Be concise. End with exactly three sections: Recommendation, Critical risks, Completion checks.
```

At the completion gate, ask whether the result is ready to report complete and request only actionable gaps.

## Fallback

If no Task subagent can be launched, perform a clearly separated second-pass review using the same prompt contract. State that independent review and model escalation were unavailable. Never claim that the native Advisor tool or any fallback reviewer ran unless that consultation actually returned a response.

## Final Report

Include whether native Advisor was unavailable, the number and timing of fallback consultations, the model used or downgrade, material advice followed or rejected, verification status and checks rerun after adviser-driven changes, and residual risk. Do not expose hidden reasoning or paste the full consultation transcript.
