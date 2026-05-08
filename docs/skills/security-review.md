# security-review

Multi-pass security review using parallel `security-auditor` subagents per concern.

## Workflow

1. Establish diff scope: `git diff origin/main...HEAD --stat`.
2. Spawn `security-auditor` subagents in parallel, one per concern:
   - Injection (SQL/NoSQL, command, template, deserialization, prompt injection in LLM-touching code)
   - Authn/Authz (token handling, sessions, RBAC, privilege escalation)
   - Secrets (hard-coded creds, leaked keys, log redaction gaps)
   - Supply chain (new/updated deps, lockfile integrity, pinning)
   - IaC (open security groups, public buckets, missing encryption)
   - Business logic (state-machine bypasses, atomicity, replay/race)
3. Each subagent verifies findings against actual code behavior — pattern matches alone are not enough.
4. Combine results, dedupe, rank by severity.

## Final report

Lead with verdict: `Ready to Merge` / `Needs Attention` / `Needs Work`. List findings by severity (Critical → Info) with file:line, what fails, why it matters, fix direction. Cite OWASP / CWE IDs. Redact discovered secrets.

## Install

```sh
gh skill install s-hiraoku/claude-harnesses security-review --scope project
```

Part of `review-pack`. Slash command: `/security-review`.
