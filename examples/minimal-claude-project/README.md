# minimal-claude-project

The smallest claude-harnesses adoption: a `CLAUDE.md`, a `.claude/settings.json`, and a ledger.

## Install

```sh
bash /path/to/claude-harnesses/scripts/install.sh \
  --target . \
  --claude-md strict \
  --settings default \
  --ledger
```

## Next steps

- Add `safety-pack` for guardrails: `--pack safety`.
- Add `verification-pack` for the Stop hook: `--pack verification`.
