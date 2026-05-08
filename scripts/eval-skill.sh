#!/usr/bin/env bash
# Bookkeeping helper for the empirical-prompt-tuning evaluation flow.
#
# Subcommands:
#   init <skill>         Scaffold evals/<skill>/{scenarios.yaml,runs/,ledger.md}
#                        from evals/_template/.
#   new-run <skill>      Create a new timestamped run file under
#                        evals/<skill>/runs/ from the run.md template.
#   status [<skill>]     Show current iteration count and last ledger entry.
#                        With no args, lists every skill that has an evals/ dir.
#
# This script does NOT spawn subagents. The actual evaluation loop runs inside
# Claude Code via the Task tool, following skills/empirical-prompt-tuning/SKILL.md.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
EVALS_DIR="${ROOT}/evals"
TEMPLATE_DIR="${EVALS_DIR}/_template"

usage() {
  cat <<'USAGE'
Usage: scripts/eval-skill.sh <subcommand> [args]

Subcommands:
  init <skill>       Scaffold evals/<skill>/ from the template.
  new-run <skill>    Create a fresh timestamped run note.
  status [<skill>]   Show current iteration / last ledger entry.
  -h, --help         This message.
USAGE
}

fail() {
  echo "error: $*" >&2
  exit 1
}

ensure_skill_exists() {
  local skill="$1"
  [[ -f "${ROOT}/skills/${skill}/SKILL.md" ]] \
    || fail "no skill at skills/${skill}/SKILL.md"
}

cmd_init() {
  local skill="${1:-}"
  [[ -n "${skill}" ]] || fail "init needs a skill name"
  ensure_skill_exists "${skill}"

  local target="${EVALS_DIR}/${skill}"
  if [[ -e "${target}" ]]; then
    fail "${target} already exists; refusing to overwrite"
  fi

  mkdir -p "${target}/runs"

  sed "s/<skill-name>/${skill}/g" "${TEMPLATE_DIR}/scenarios.yaml" > "${target}/scenarios.yaml"
  sed "s/<skill-name>/${skill}/g" "${TEMPLATE_DIR}/ledger.md" > "${target}/ledger.md"

  echo "scaffolded ${target}/"
  echo "next: edit ${target}/scenarios.yaml, then 'scripts/eval-skill.sh new-run ${skill}'"
}

cmd_new_run() {
  local skill="${1:-}"
  [[ -n "${skill}" ]] || fail "new-run needs a skill name"
  ensure_skill_exists "${skill}"

  local target="${EVALS_DIR}/${skill}"
  [[ -d "${target}" ]] || fail "no evals/${skill} yet; run 'init' first"

  local timestamp
  timestamp="$(date -u +"%Y%m%dT%H%M%SZ")"
  local run_file="${target}/runs/${timestamp}.md"

  local skill_commit
  skill_commit="$(git -C "${ROOT}" log -1 --format='%h' "skills/${skill}/SKILL.md" 2>/dev/null || echo "uncommitted")"

  local iteration
  iteration="$(find "${target}/runs" -maxdepth 1 -name '*.md' | wc -l | tr -d ' ')"

  sed \
    -e "s|<skill-name>|${skill}|g" \
    -e "s|<git rev-parse HEAD of skills/${skill}>|${skill_commit}|g" \
    -e "s|<UTC ISO timestamp>|$(date -u +"%Y-%m-%dT%H:%M:%SZ")|g" \
    -e "s|^- Iteration: \`N\`|- Iteration: \`${iteration}\`|" \
    "${TEMPLATE_DIR}/run.md" > "${run_file}"

  echo "created ${run_file}"
  echo "next: dispatch subagents per scenarios.yaml, fill in this file, append a ledger entry"
}

cmd_status() {
  local skill="${1:-}"

  if [[ -z "${skill}" ]]; then
    if [[ ! -d "${EVALS_DIR}" ]]; then
      echo "no evals/ directory yet"
      return
    fi
    while IFS= read -r dir; do
      local name
      name="$(basename "${dir}")"
      [[ "${name}" == _template ]] && continue
      cmd_status "${name}"
      echo
    done < <(find "${EVALS_DIR}" -mindepth 1 -maxdepth 1 -type d | sort)
    return
  fi

  local target="${EVALS_DIR}/${skill}"
  [[ -d "${target}" ]] || fail "no evals/${skill}"

  local runs
  runs="$(find "${target}/runs" -maxdepth 1 -name '*.md' 2>/dev/null | wc -l | tr -d ' ')"
  echo "skill: ${skill}"
  echo "  runs recorded: ${runs}"

  if [[ -f "${target}/ledger.md" ]]; then
    local last_entry
    last_entry="$(grep -E '^- [0-9]{4}-[0-9]{2}-[0-9]{2}' "${target}/ledger.md" | tail -1 || true)"
    if [[ -n "${last_entry}" ]]; then
      echo "  last ledger entry: ${last_entry}"
    else
      echo "  last ledger entry: (none yet)"
    fi
  fi
}

case "${1:-}" in
  init) shift; cmd_init "$@" ;;
  new-run) shift; cmd_new_run "$@" ;;
  status) shift; cmd_status "$@" ;;
  -h|--help|"") usage ;;
  *) fail "unknown subcommand: $1" ;;
esac
