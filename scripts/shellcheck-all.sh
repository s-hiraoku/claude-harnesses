#!/usr/bin/env bash
# Run shellcheck against every committed shell script.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

if ! command -v shellcheck >/dev/null 2>&1; then
  echo "shellcheck not installed; skipping"
  exit 0
fi

cd "${ROOT}"
shellcheck -x scripts/*.sh plugins/*/scripts/*.sh
echo "shellcheck passed"
