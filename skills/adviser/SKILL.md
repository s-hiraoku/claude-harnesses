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

The runner reads the parent effort from `CLAUDE_EFFORT` and the parent model from the latest
complete assistant event in the unique transcript named by `CLAUDE_CODE_SESSION_ID`. Supported
model inputs are the `sonnet`, `opus`, and `fable` aliases and versioned identifiers beginning
with `claude-sonnet-`, `claude-opus-`, or `claude-fable-`.

## Workflow

1. Check for native Advisor. Do not run both native Advisor and this fallback for ceremony.
2. Orient before consulting. Gather only the repository evidence needed for a useful review.
3. Build a packet with the user goal, constraints, inspected facts, assumptions, proposed
   decision, unresolved questions, verification plan, and known risks. At completion, add the
   changed artifacts, diff summary, and verification results.
4. Pipe the packet to `scripts/run_adviser.py` from this skill directory:

   ```bash
   python3 <adviser-skill-directory>/scripts/run_adviser.py <<'EOF'
   <consultation packet>
   EOF
   ```

   Normally omit `--model` and `--effort`; automatic parent detection is the safety boundary.
   Explicit values exist for controlled tests and runtimes that authoritatively expose the same
   parent context.
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
clearly separated self-review without claiming an Adviser ran.
