#!/usr/bin/env bash
# PostToolUse hook: format the file that was just edited or written.
set -euo pipefail

# shellcheck source=/dev/null
source "$(dirname "${BASH_SOURCE[0]}")/../_shared/hook-prelude.sh"

if [[ -z "${HOOK_FILE_PATH}" || ! -f "${HOOK_FILE_PATH}" ]]; then
  exit 0
fi

run() {
  echo "format-on-edit: $*" >&2
  "$@" >/dev/null 2>&1 || true
}

case "${HOOK_FILE_PATH}" in
  *.ts|*.tsx|*.js|*.jsx|*.mjs|*.cjs|*.json|*.md|*.css|*.scss|*.html|*.yml|*.yaml)
    if command -v prettier >/dev/null 2>&1; then
      run prettier --write "${HOOK_FILE_PATH}"
    fi
    ;;
  *.py)
    if command -v ruff >/dev/null 2>&1; then
      run ruff format "${HOOK_FILE_PATH}"
    elif command -v black >/dev/null 2>&1; then
      run black --quiet "${HOOK_FILE_PATH}"
    fi
    ;;
  *.go)
    if command -v gofmt >/dev/null 2>&1; then
      run gofmt -w "${HOOK_FILE_PATH}"
    fi
    ;;
  *.rs)
    if command -v rustfmt >/dev/null 2>&1; then
      run rustfmt --quiet "${HOOK_FILE_PATH}"
    fi
    ;;
esac

exit 0
