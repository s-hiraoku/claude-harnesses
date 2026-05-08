#!/usr/bin/env bash
# CI helper: validate every plugin.json and the marketplace.json against schema.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

cd "${ROOT}"

python3 -m jsonschema -i ".claude-plugin/marketplace.json" "schemas/marketplace.schema.json"

while IFS= read -r manifest; do
  echo "validate ${manifest}"
  python3 -m jsonschema -i "${manifest}" "schemas/plugin.schema.json"
done < <(find plugins -mindepth 3 -name plugin.json -path "*/.claude-plugin/*" | sort)

echo "all plugin manifests valid"
