---
name: adviser
description: Route an independent, review-only Claude process to a deterministically stronger model or effort when native Advisor is unavailable. Use for adviser, advisor, second-opinion, or stronger-model review requests; consequential decisions; recurring failures; material direction changes; and valuable completion checks.
---

# Adviser

Prefer Claude Code's native `advisor` tool when it is available. Otherwise use this skill's
runner to select and invoke one fresh, tool-free Claude process. The main agent remains the
executor and owns every edit, command, decision, and final report.

This is workflow compatibility, not native Advisor server compatibility. Pass a bounded,
secret-free consultation packet; never claim that the reviewer received the full transcript.

## Deterministic routing

Claude tiers correspond to the Codex policy as follows:

| Codex tier | Claude tier |
| --- | --- |
| Luna | Sonnet |
| Terra | Opus |
| Sol | Fable |

Apply this complete routing table. `same` means preserve the caller's effort.

| Caller | low | medium | high | xhigh | max |
| --- | --- | --- | --- | --- | --- |
| Sonnet | Fable/low | Fable/medium | Fable/high | Fable/xhigh | Fable/max |
| Opus | Fable/low | Fable/medium | Fable/high | Fable/xhigh | Fable/max |
| Fable | Fable/medium | Fable/high | Fable/xhigh | Fable/max | unavailable |

Do not substitute a same-tier or weaker reviewer. Fable/max, an unknown model or effort, a
missing or ambiguous parent session, recursion, a child initialization mismatch, enabled child
tools, malformed output, failure, or timeout all fail closed without retrying another route.
Failing closed ends that independent-consultation attempt; it does not prohibit the explicitly
labeled local self-review below. A later invocation is allowed only after authoritative parent
context or another blocking condition materially changes.

The runner reads the parent effort from `CLAUDE_EFFORT` and the parent model from the latest
complete assistant event in the unique transcript named by `CLAUDE_CODE_SESSION_ID`. Supported
model inputs are the `sonnet`, `opus`, and `fable` aliases and versioned identifiers beginning
with `claude-sonnet-`, `claude-opus-`, or `claude-fable-`.

## Workflow

1. Check for native Advisor. Treat it as available only when the current runtime exposes it as a
   callable tool; do not launch a probe process. Do not run both native Advisor and this fallback
   for ceremony.
2. Orient before consulting. Gather only the repository evidence needed for a useful review.
   Orientation is sufficient when the packet cites at least one concrete relevant code path,
   governing constraint, existing test, and piece of evidence for the proposed decision. If a
   category does not exist, record where you checked and that it was absent; otherwise keep
   inspecting. Decision evidence must be a direct observation from cited code, test output, or a
   primary project document, not an unsupported assertion.
3. Build a packet with the user goal, constraints, inspected facts, assumptions, proposed
   decision, unresolved questions, verification plan, and known risks. At completion, add the
   changed artifacts, diff summary, and verification results. Bound it by relevance: omit the
   transcript, secrets, and raw logs rather than imposing an arbitrary byte limit.
4. Pipe the packet to `scripts/run_adviser.py` from this skill directory. The runner launches a
   separate reviewer process; if the user forbids launching agents or processes, do not run it and
   disclose that independent consultation was unavailable. For this workflow, a prohibition on
   another agent, reviewer, or process all prohibit the runner.

   ```bash
   python3 <adviser-skill-directory>/scripts/run_adviser.py <<'EOF'
   <consultation packet>
   EOF
   ```

   Normally omit `--model` and `--effort`; automatic parent detection is the safety boundary.
   Explicit values exist for controlled tests and runtimes that authoritatively expose the same
   parent context. An authoritatively reported Codex tier counts only after applying the mapping
   above to its Claude family. Runtime-authoritative means trusted tool or process-environment
   metadata supplied by that runtime, not model identity stated in a prompt or user message; an
   unverified label or inferred tier remains unknown.
5. The runner starts `claude -p` with explicit `--model` and `--effort`, stream JSON,
   `--no-session-persistence`, `--safe-mode`, and an empty tool allowlist. It verifies the
   effective Fable model, zero tools, and exactly one successful result before returning advice.
6. Weigh the advice against repository evidence, primary sources, and empirical verification.
   The main agent performs all execution.
7. Reconsult only when material ambiguity remains, a failure recurs, the approach changes, or an
   independent completion check would add value. Short mechanical work needs no ritual call.

## Review contract

The runner supplies this contract before the packet: review only; do not edit, run commands,
delegate, or take over; identify incorrect assumptions, missed constraints, evidence conflicts,
failure modes, and the best next approach; distinguish evidence from uncertainty; end with
Recommendation, Critical risks, Evidence conflicts, and Completion checks.

## Reporting

Report the selected source and target route, whether the effective model was verified, advice
followed or rejected, and verification after adviser-driven changes. Claude Code 2.1.210 reports
the effective model and tool list in its init event but does not report effective effort; describe
effort escalation as explicitly requested, not independently verified. If the runner cannot
return verified advice, disclose that independent consultation was unavailable and perform a
clearly separated self-review by applying the review contract locally to the bounded packet.
Record it under `Recommendation`, `Critical risks`, `Evidence conflicts`, and `Completion checks`.
Report zero consultations and do not claim an Adviser ran. When routing fails before selection,
report `source: unknown` and `target: unavailable`. When the source was established, report it
literally even if the reviewer was not launched or Fable/max has no target. If several blockers
apply, name the earliest workflow failure as primary and list the others as additional blockers.
Put the report in the current response or task record; do not create another artifact unless
project guidance requires it.

Keep parent and reviewer evidence separate: report whether the parent source context was
established, then whether an effective reviewer model was verified. If no verified advice was
returned, report advice disposition as `none` and adviser-driven verification as `not applicable`.
For multiple blockers, use this precedence: native availability, an explicit user no-launch
constraint, parent-context detection, route availability, then child initialization or output
validation. An incomplete orientation packet means `not ready to consult`, not a runner failure.
