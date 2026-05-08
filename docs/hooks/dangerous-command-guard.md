# dangerous-command-guard

PreToolUse guard that blocks obviously dangerous shell commands.

## Trigger

- Event: `PreToolUse`
- Matcher: `Bash`

## What it blocks

- `rm -rf /` and `~`/`$HOME` variants
- `git push --force` / `-f`
- `git reset --hard`
- `chmod -R 777`
- `dd of=/dev/sd*` / `nvme*` / `disk*`
- `cat`/`tail`/`head` on `id_rsa`/`id_ed25519`/`*.pem`
- `cat`/`grep`/`sed` on `.env`
- `curl ... | sh` and `wget ... | sh`

## Exit codes

- `0` — allow
- `2` — block

## Kill switches

- `CLAUDE_HARNESSES_DISABLE=1`

## Notes

Pattern matches are intentionally narrow to minimize false positives. Operators on `/dev/loop*`, `/dev/xvd*`, `/dev/mapper/*` are not matched — widen the regex if your environment exposes those.

Pack: [safety-pack](../packs/safety-pack.md)
