#!/usr/bin/env bash
# PostToolUse hook: run a quick typecheck scoped to the changed file.
# Non-blocking by design; surfaces type errors as PostToolUse stderr so they
# enter Claude's context.
set -euo pipefail

# shellcheck source=/dev/null
source "$(dirname "${BASH_SOURCE[0]}")/../../_shared/hook-prelude.sh"

if [[ -z "${HOOK_FILE_PATH}" || ! -f "${HOOK_FILE_PATH}" ]]; then
  exit 0
fi

case "${HOOK_FILE_PATH}" in
  *.ts|*.tsx)
    if command -v tsc >/dev/null 2>&1 && [[ -f tsconfig.json ]]; then
      tsc --noEmit -p . --pretty false >&2 || true
    fi
    ;;
  *.py)
    if command -v mypy >/dev/null 2>&1; then
      mypy --no-color-output --hide-error-context "${HOOK_FILE_PATH}" >&2 || true
    fi
    ;;
esac

exit 0
