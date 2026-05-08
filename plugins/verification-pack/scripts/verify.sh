#!/usr/bin/env bash
# Wrapper that delegates to the project's scripts/verify.sh when present,
# otherwise runs a sane default for the detected toolchain.
set -euo pipefail

if [[ -x "scripts/verify.sh" ]]; then
  exec bash scripts/verify.sh "$@"
fi

if command -v npm >/dev/null 2>&1 && [[ -f package.json ]]; then
  npm run lint --if-present
  npm run typecheck --if-present
  npm test --if-present --silent
elif command -v ruff >/dev/null 2>&1 && [[ -f pyproject.toml ]]; then
  ruff check .
  command -v pytest >/dev/null 2>&1 && pytest || true
else
  echo "verification-pack: no scripts/verify.sh and no recognized toolchain" >&2
  exit 1
fi
