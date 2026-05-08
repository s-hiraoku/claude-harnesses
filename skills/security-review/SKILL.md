---
name: security-review
description: Run a multi-pass security review over the current diff using parallel specialist subagents focused on injection, authn/authz, secrets, supply-chain, and infrastructure-as-code risks.
---

# Security Review

Use this workflow before merging or releasing change sets that touch authentication, data handling, network surface, infrastructure-as-code, or third-party dependencies.

## Workflow

1. Establish the diff scope: `git diff origin/main...HEAD --stat` and a list of changed files.
2. Spawn the `security-auditor` subagent in parallel for each concern below. Each subagent reads only the diff plus immediately relevant context.
   - **Injection**: SQL/NoSQL, command, template, deserialization, prompt injection in LLM-touching code.
   - **Authn/Authz**: token handling, session, RBAC checks, privilege escalation.
   - **Secrets**: hard-coded credentials, leaked keys, insufficient redaction in logs.
   - **Supply chain**: new or updated dependencies, lockfile integrity, pinned versions.
   - **Infrastructure-as-code**: open security groups, public buckets, missing encryption, weak defaults.
   - **Business logic**: state-machine bypasses, atomicity violations, replay/race conditions.
3. Each subagent returns findings ranked by severity with file/line citations.
4. Verify each candidate finding against actual code behavior to filter false positives.
5. Combine and dedupe results into a single severity-ordered list.

## Constraints

- Do not exfiltrate secrets discovered during review; redact in the report.
- Treat "best practice" suggestions as low priority unless they map to a concrete risk.
- Cite OWASP Top 10 / CWE IDs where they sharpen the finding.

## Final Report

Lead with verdict: `Ready to Merge` / `Needs Attention` / `Needs Work`. Then list findings by severity (Critical / High / Medium / Low / Info) with file, line, what fails, why it matters, and a concrete fix direction. End with verification reviewed and remaining gaps.
