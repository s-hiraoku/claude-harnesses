#!/usr/bin/env bash
# SessionEnd hook: append a brief end-of-session marker to the ledger.
set -euo pipefail

# shellcheck source=/dev/null
source "$(dirname "${BASH_SOURCE[0]}")/../../_shared/hook-prelude.sh"

if [[ -z "${REPO_ROOT}" || ! -f "${REPO_ROOT}/ledger/current.md" ]]; then
  exit 0
fi

timestamp="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
{
  echo
  echo "### ${timestamp} session end"
  echo
  echo "- Session ended."
} >> "${REPO_ROOT}/ledger/current.md"

exit 0
