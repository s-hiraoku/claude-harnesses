---
description: Run a multi-pass security review using the security-review skill and parallel security-auditor subagents.
argument-hint: "[diff scope]"
---

Run the `security-review` skill against $ARGUMENTS (or the current branch diff if empty).

Spawn `security-auditor` subagents in parallel, one per concern (injection, authn/authz, secrets, supply-chain, IaC, business-logic). Combine and dedupe findings, rank by severity, and end with a one-line verdict.
