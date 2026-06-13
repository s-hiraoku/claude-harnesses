#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

TARGET="."
CLAUDE_MD_TEMPLATE=""
SETTINGS=""
SKILLS=""
PACKS=()
INSTALL_VERIFY=1
INSTALL_LEDGER=0
INSTALL_MCP=0
DRY_RUN=0
FORCE=0

usage() {
  cat <<'USAGE'
Usage: scripts/install.sh [options]

Selectively copy claude-harnesses files into a target project.

Options:
  --target DIR              Target project directory. Defaults to current directory.
  --pack NAME               Install a plugin pack: safety, verification, review, tdd,
                            pr-guardian, long-running, mcp, product, research,
                            meta, teaching, full. Repeatable.
  --claude-md NAME          Install templates/claude-md/NAME/CLAUDE.md as ./CLAUDE.md.
                            Available: strict, frontend, library, nextjs.
  --settings NAME           Install settings/NAME.json as .claude/settings.json.
                            Available: strict, default, experimental.
  --skills LIST             Install comma-separated skills, or "all".
  --ledger                  Install ledger templates.
  --mcp                     Install plugins/mcp-pack/.mcp.json into target.
  --no-verify               Skip installing scripts/verify.sh (installed by default).
  --force                   Overwrite existing target files.
  --dry-run                 Print actions only.
  -h, --help                Show this help.

Examples:
  scripts/install.sh --target /path --pack safety --pack verification --pack pr-guardian \
                     --claude-md strict --settings default --ledger
  scripts/install.sh --target . --skills tdd,review
USAGE
}

fail() {
  echo "error: $*" >&2
  exit 1
}

log() { echo "$*"; }

canonical_existing_path() {
  local path="$1" dir
  [[ -e "${path}" ]] || return 1
  dir="$(cd "$(dirname "${path}")" && pwd -P)"
  printf '%s/%s\n' "${dir}" "$(basename "${path}")"
}

same_existing_path() {
  local left="$1" right="$2"
  [[ -e "${left}" && -e "${right}" ]] || return 1
  [[ "$(canonical_existing_path "${left}")" == "$(canonical_existing_path "${right}")" ]]
}

copy_file() {
  local src="$1" dest="$2"
  if same_existing_path "${src}" "${dest}"; then
    log "skip same path ${dest}"
    return
  fi
  if [[ -e "${dest}" && "${FORCE}" -ne 1 ]]; then
    log "skip existing ${dest}"
    return
  fi
  log "install ${dest}"
  if [[ "${DRY_RUN}" -eq 1 ]]; then return; fi
  mkdir -p "$(dirname "${dest}")"
  cp "${src}" "${dest}"
}

copy_dir() {
  local src="$1" dest="$2"
  if same_existing_path "${src}" "${dest}"; then
    log "skip same path ${dest}"
    return
  fi
  if [[ -e "${dest}" && "${FORCE}" -ne 1 ]]; then
    log "skip existing ${dest}"
    return
  fi
  log "install ${dest}/"
  if [[ "${DRY_RUN}" -eq 1 ]]; then return; fi
  rm -rf "${dest}"
  mkdir -p "$(dirname "${dest}")"
  cp -R "${src}" "${dest}"
}

merge_hooks_json() {
  local src="$1" dest="$2"
  if ! command -v jq >/dev/null 2>&1; then
    fail "jq is required to merge hook JSON; install jq or skip the pack"
  fi
  if [[ ! -f "${dest}" ]]; then
    log "create ${dest}"
    if [[ "${DRY_RUN}" -eq 1 ]]; then return; fi
    mkdir -p "$(dirname "${dest}")"
    jq '{ hooks: . }' "${src}" > "${dest}"
    return
  fi
  log "merge hooks into ${dest}"
  if [[ "${DRY_RUN}" -eq 1 ]]; then return; fi
  local tmp
  tmp="$(mktemp)"
  # Append per-event hook arrays into the existing settings.json. Never replace.
  jq -s '
    .[0] as $existing | .[1] as $incoming |
    $existing
    | .hooks = ((.hooks // {}) as $h |
        ($incoming | to_entries | reduce .[] as $event ($h;
          .[$event.key] = ((.[$event.key] // []) + $event.value)
        ))
      )
  ' "${dest}" "${src}" > "${tmp}"
  mv "${tmp}" "${dest}"
}

FUNCTIONAL_PACKS=(
  safety
  verification
  review
  tdd
  pr-guardian
  long-running
  product
  research
  meta
  teaching
)

install_pack() {
  local pack="$1"

  if [[ "${pack}" == "full" ]]; then
    for sub in "${FUNCTIONAL_PACKS[@]}"; do
      install_pack "${sub}"
    done
    copy_file "${ROOT}/plugins/mcp-pack/.mcp.json" "${TARGET}/.mcp.json"
    return
  fi

  if [[ "${pack}" == "mcp" ]]; then
    copy_file "${ROOT}/plugins/mcp-pack/.mcp.json" "${TARGET}/.mcp.json"
    return
  fi

  local pack_dir="${ROOT}/plugins/${pack}-pack"
  [[ -d "${pack_dir}" ]] || fail "unknown pack: ${pack}"

  if [[ -d "${pack_dir}/skills" ]]; then
    while IFS= read -r d; do
      local name
      name="$(basename "${d}")"
      copy_dir "${ROOT}/skills/${name}" "${TARGET}/.claude/skills/${name}"
    done < <(find "${pack_dir}/skills" -mindepth 1 -maxdepth 1 \( -type d -o -type l \))
  fi

  if [[ -d "${pack_dir}/agents" ]]; then
    while IFS= read -r f; do
      copy_file "${f}" "${TARGET}/.claude/agents/$(basename "${f}")"
    done < <(find "${pack_dir}/agents" -mindepth 1 -maxdepth 1 -type f -name "*.md")
  fi

  if [[ -d "${pack_dir}/commands" ]]; then
    while IFS= read -r f; do
      copy_file "${f}" "${TARGET}/.claude/commands/$(basename "${f}")"
    done < <(find "${pack_dir}/commands" -mindepth 1 -maxdepth 1 -type f -name "*.md")
  fi

  if [[ -d "${pack_dir}/scripts" ]]; then
    copy_dir "${pack_dir}/scripts" "${TARGET}/.claude/hooks/${pack}-pack"
  fi

  if [[ -f "${pack_dir}/hooks.json" ]]; then
    merge_hooks_json "${pack_dir}/hooks.json" "${TARGET}/.claude/settings.json"
  fi

  if [[ "${pack}" == "long-running" && -d "${pack_dir}/ledger" ]]; then
    copy_dir "${pack_dir}/ledger" "${TARGET}/ledger"
  fi
}

while [[ "$#" -gt 0 ]]; do
  case "$1" in
    --target) TARGET="${2:-}"; [[ -n "${TARGET}" ]] || fail "--target requires a directory"; shift 2 ;;
    --pack) PACKS+=("${2:-}"); [[ -n "${2:-}" ]] || fail "--pack requires a name"; shift 2 ;;
    --claude-md) CLAUDE_MD_TEMPLATE="${2:-}"; shift 2 ;;
    --settings) SETTINGS="${2:-}"; shift 2 ;;
    --skills) SKILLS="${2:-}"; shift 2 ;;
    --ledger) INSTALL_LEDGER=1; shift ;;
    --mcp) INSTALL_MCP=1; shift ;;
    --no-verify) INSTALL_VERIFY=0; shift ;;
    --force) FORCE=1; shift ;;
    --dry-run) DRY_RUN=1; shift ;;
    -h|--help) usage; exit 0 ;;
    *) fail "unknown option: $1" ;;
  esac
done

[[ -d "${TARGET}" ]] || fail "target directory does not exist: ${TARGET}"
TARGET="$(cd "${TARGET}" && pwd)"

if [[ -n "${CLAUDE_MD_TEMPLATE}" ]]; then
  src="${ROOT}/templates/claude-md/${CLAUDE_MD_TEMPLATE}/CLAUDE.md"
  [[ -f "${src}" ]] || fail "unknown CLAUDE.md template: ${CLAUDE_MD_TEMPLATE}"
  copy_file "${src}" "${TARGET}/CLAUDE.md"
fi

if [[ -n "${SETTINGS}" ]]; then
  src="${ROOT}/settings/${SETTINGS}.json"
  [[ -f "${src}" ]] || fail "unknown settings preset: ${SETTINGS}"
  copy_file "${src}" "${TARGET}/.claude/settings.json"
fi

if [[ "${INSTALL_VERIFY}" -eq 1 ]]; then
  copy_file "${ROOT}/scripts/verify.sh" "${TARGET}/scripts/verify.sh"
fi

if [[ "${INSTALL_LEDGER}" -eq 1 ]]; then
  copy_dir "${ROOT}/ledger" "${TARGET}/ledger"
fi

if [[ "${INSTALL_MCP}" -eq 1 ]]; then
  copy_file "${ROOT}/plugins/mcp-pack/.mcp.json" "${TARGET}/.mcp.json"
fi

if [[ -n "${SKILLS}" ]]; then
  if [[ "${SKILLS}" == "all" ]]; then
    while IFS= read -r d; do
      name="$(basename "${d}")"
      copy_dir "${d}" "${TARGET}/.claude/skills/${name}"
    done < <(find "${ROOT}/skills" -mindepth 1 -maxdepth 1 -type d | sort)
  else
    IFS=',' read -ra skill_names <<<"${SKILLS}"
    for name in "${skill_names[@]}"; do
      [[ -n "${name}" ]] || continue
      [[ -f "${ROOT}/skills/${name}/SKILL.md" ]] || fail "unknown skill: ${name}"
      copy_dir "${ROOT}/skills/${name}" "${TARGET}/.claude/skills/${name}"
    done
  fi
fi

if [[ "${#PACKS[@]}" -gt 0 ]]; then
  for pack in "${PACKS[@]}"; do
    install_pack "${pack}"
  done
fi

log "claude harness deployment complete"
