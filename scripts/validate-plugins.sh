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

# Install-safety: a plugin is copied into a cache by source dir alone, so no
# auto-discovered component (or its symlink) may resolve outside the plugin
# root. Symlinks are fine as long as the link lives inside the plugin and
# points at something that exists (Claude Code dereferences and copies it).
echo "checking component paths stay inside each plugin root"
escapes=0
for plugin_dir in plugins/*/; do
  base="$(basename "${plugin_dir}")"
  [[ "${base}" == _* ]] && continue
  abs_root="$(cd "${plugin_dir}" && pwd)"
  for kind in skills agents commands; do
    comp="${plugin_dir}${kind}"
    [[ -d "${comp}" ]] || continue
    for entry in "${comp}"/*; do
      [[ -e "${entry}" || -L "${entry}" ]] || continue
      if [[ ! -e "${entry}" ]]; then
        echo "ERROR ${base}: ${kind}/$(basename "${entry}") is a dangling symlink"
        escapes=1
        continue
      fi
      resolved="$(cd "$(dirname "${entry}")" && pwd)/$(basename "${entry}")"
      case "${resolved}" in
        "${abs_root}"/*) : ;;
        *) echo "ERROR ${base}: ${kind}/$(basename "${entry}") escapes plugin root"; escapes=1 ;;
      esac
    done
  done
done
if [[ "${escapes}" -ne 0 ]]; then
  echo "component path validation failed"
  exit 1
fi
echo "all component paths stay inside their plugin root"
