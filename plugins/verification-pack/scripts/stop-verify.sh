#!/usr/bin/env bash
# Stop hook: run scripts/verify.sh from the repo root and block the stop on
# failure. Honors `stop_hook_active` so we never get into an infinite loop.
set -euo pipefail

# shellcheck source=/dev/null
source "$(dirname "${BASH_SOURCE[0]}")/../_shared/hook-prelude.sh"

# Reentrancy guard: if Claude is already inside a previously-blocked Stop, let
# it finish.
if printf '%s' "${HOOK_INPUT}" | grep -q '"stop_hook_active"[[:space:]]*:[[:space:]]*true'; then
  exit 0
fi

if [[ -z "${REPO_ROOT}" || ! -x "${REPO_ROOT}/scripts/verify.sh" ]]; then
  echo "stop-verify: no scripts/verify.sh found at repo root; skipping" >&2
  exit 0
fi

cd "${REPO_ROOT}"
if bash scripts/verify.sh; then
  exit 0
fi

echo "stop-verify: scripts/verify.sh failed; continuing the session to address it" >&2
exit 2
