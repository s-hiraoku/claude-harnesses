# Shared bash prelude for hook scripts.
# Source with: source "${CLAUDE_PLUGIN_ROOT}/../_shared/hook-prelude.sh"
# Sets:
#   - exit 0 immediately if CLAUDE_HARNESSES_DISABLE=1
#   - HOOK_INPUT  : raw stdin
#   - HOOK_FILE_PATH : .tool_input.file_path extracted via jq, or empty
#   - REPO_ROOT  : git rev-parse top-level, or empty when not inside git

if [[ "${CLAUDE_HARNESSES_DISABLE:-}" == "1" ]]; then
  exit 0
fi

HOOK_INPUT="$(cat || true)"

HOOK_FILE_PATH=""
if command -v jq >/dev/null 2>&1; then
  HOOK_FILE_PATH="$(printf '%s' "${HOOK_INPUT}" | jq -r '.tool_input.file_path // empty' 2>/dev/null || true)"
fi

REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || true)"
