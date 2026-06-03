#!/usr/bin/env bash
# SessionStart hook: inject git status + ledger head as additional context.
set -euo pipefail

# shellcheck source=/dev/null
source "$(dirname "${BASH_SOURCE[0]}")/../_shared/hook-prelude.sh"

if [[ -z "${REPO_ROOT}" ]]; then
  exit 0
fi

cd "${REPO_ROOT}"

echo "## Repository state"
echo
echo "- Branch: $(git branch --show-current 2>/dev/null || echo "unknown")"

short_status="$(git status --short 2>/dev/null | head -10 || true)"
if [[ -n "${short_status}" ]]; then
  echo "- Working tree changes:"
  while IFS= read -r line; do
    printf '  - %s\n' "${line}"
  done <<<"${short_status}"
else
  echo "- Working tree: clean"
fi

if [[ -f "ledger/current.md" ]]; then
  echo
  echo "## Active task ledger (head)"
  echo
  awk 'NR>1 && NR<=31' ledger/current.md
fi

exit 0
