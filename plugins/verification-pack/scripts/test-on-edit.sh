#!/usr/bin/env bash
# PostToolUse hook: run only the tests related to the file that was just edited.
# Non-blocking; failure output is surfaced to stderr.
set -euo pipefail

# shellcheck source=/dev/null
source "$(dirname "${BASH_SOURCE[0]}")/../_shared/hook-prelude.sh"

if [[ -z "${HOOK_FILE_PATH}" || ! -f "${HOOK_FILE_PATH}" ]]; then
  exit 0
fi

# find with prune so node_modules / .venv / .git / dist / build do not slow us
# down on large repos.
locate_test() {
  local pattern_a="$1" pattern_b="$2"
  find . \
    \( -path ./node_modules -o -path ./.venv -o -path ./.git \
       -o -path ./dist -o -path ./build -o -path ./target \
       -o -path ./site \) -prune \
    -o \( -name "${pattern_a}" -o -name "${pattern_b}" \) -print 2>/dev/null \
    | head -1
}

base="$(basename "${HOOK_FILE_PATH}")"
stem="${base%.*}"

case "${HOOK_FILE_PATH}" in
  *test*|*spec*|*__tests__*)
    target="${HOOK_FILE_PATH}"
    ;;
  *.py)
    target="$(locate_test "test_${stem}.py" "${stem}_test.py")"
    ;;
  *.ts|*.tsx|*.js|*.jsx)
    target="$(locate_test "${stem}.test.*" "${stem}.spec.*")"
    ;;
  *)
    target=""
    ;;
esac

if [[ -z "${target}" || ! -f "${target}" ]]; then
  exit 0
fi

case "${target}" in
  *.py)
    if command -v pytest >/dev/null 2>&1; then
      echo "test-on-edit: pytest ${target}" >&2
      pytest "${target}" >&2 || true
    fi
    ;;
  *.ts|*.tsx|*.js|*.jsx|*.mjs|*.cjs)
    if [[ -f package.json ]] && command -v npx >/dev/null 2>&1; then
      echo "test-on-edit: vitest/jest ${target}" >&2
      npx --no-install vitest run "${target}" >&2 2>/dev/null \
        || npx --no-install jest "${target}" >&2 2>/dev/null \
        || true
    fi
    ;;
esac

exit 0
