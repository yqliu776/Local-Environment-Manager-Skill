# Query Rules

## Source Order
- Read `env.json` first.
- Read `environment.zh-CN.md` or `environment.en.md` only when a human-readable explanation is needed.
- Run `scripts/collect_env.py` when the snapshot must be refreshed.
- Query the live system ad hoc only when one targeted verification is cheaper than regenerating the snapshot.

## Refresh Triggers
- The user asks to verify or update environment facts.
- The task may change machine-level state.
- `env.json` is missing, stale, or incomplete.
- The current request depends on tools or policies not present in the snapshot.

## Collection Policy
- Use the project-local `uv` environment for this skill's scripts.
- Run `uv sync` before the first scripted operation or after dependency changes.
- Pass `--language en` for English-speaking users.
- Pass `--language zh` for Chinese-speaking users so the interactive prompts stay bilingual.
- Prefer passing user hints into `collect_env.py` rather than hardcoding assumptions in `env.json`.
- If the user explicitly says they have several environment facts or local rules to provide, convert them into script flags instead of leaving them only in the conversation.
- Use `--rule`, `--protected-path`, and `--protected-file` for do-not-touch constraints whenever the user provides them.
- Record stable conventions in `environment_management.notes`.
- Keep `agent_summary.prompt_overview` concise enough to paste into future agent prompts.
- Regenerate `environment.zh-CN.md` and `environment.en.md` from `env.json` instead of editing them manually.

## Response Style
- Return the recorded fact before doing extra probing.
- State clearly when a fact comes from cached JSON versus live verification.
- Avoid broad system inspection when one targeted check is enough.
