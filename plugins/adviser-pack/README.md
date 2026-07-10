# Adviser pack

Provides `/adviser` and the reusable `adviser` skill for Claude Code environments where the native server-side Advisor tool is unavailable.

The fallback consults a fresh, review-only Opus Task subagent at important decision and completion gates. This is an instruction-level role unless the runtime separately restricts its tools. The main agent remains responsible for all execution and verifies advice against repository evidence.
