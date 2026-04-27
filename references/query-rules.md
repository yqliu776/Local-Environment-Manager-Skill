# Query Rules

## Source Order
- Read `env.json` first.
- Read `environment.md` only when a human-readable explanation is needed.
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
- Prefer passing user hints into `collect_env.py` rather than hardcoding assumptions in `env.json`.
- Record stable conventions in `environment_management.notes`.
- Keep `agent_summary.prompt_overview` concise enough to paste into future agent prompts.
- Regenerate `environment.md` from `env.json` instead of editing it manually.

## Response Style
- Return the recorded fact before doing extra probing.
- State clearly when a fact comes from cached JSON versus live verification.
- Avoid broad system inspection when one targeted check is enough.
