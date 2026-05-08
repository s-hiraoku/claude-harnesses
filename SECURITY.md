# Security

The hooks in this repository are examples, not complete security products. They aim to reduce common foot-guns when running Claude Code autonomously. Combine them with permissions, sandboxing, code review, and CI checks before relying on them in high-risk environments.

## Kill switch

Every guard hook short-circuits to a successful exit when the environment variable `CLAUDE_HARNESSES_DISABLE` is set to `1`. Use this to recover from a misfiring hook without editing config:

```sh
export CLAUDE_HARNESSES_DISABLE=1
```

Unset the variable to re-enable hook enforcement.

## Reporting

Do not report bypasses of example hooks as vulnerabilities unless they expose secrets or create risk in this repository itself.

For production use, adapt, test, and combine these examples with maintained scanners, sandboxing, review, approval policy, and CI verification.

If you believe this repository itself exposes a secret, an unsafe workflow, or a security-sensitive defect, open a private report through GitHub Security Advisories when available, or contact the maintainer directly.

## Runtime requirements

- `python3` >= 3.10 for guard hooks.
- `jq` for `scripts/install.sh` settings.json merging.
- `bash` 4+ for shell hooks (macOS users running stock `/bin/bash` should install a newer version via Homebrew).
