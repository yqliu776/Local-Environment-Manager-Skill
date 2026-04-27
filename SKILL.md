---
name: local-environment-query
description: Collect, summarize, and reuse local development environment facts with minimal token cost. Use when Codex needs to capture machine-level setup, generate or refresh `references/env.json`, render a human-readable environment markdown file, or query concise environment facts before making system-level assumptions.
---

# Local Environment Manager

Read `references/env.json` first.

Use it as the primary source for machine-level environment facts and agent prompt compression.

Read `references/environment.md` only when a human-readable explanation is useful.

Read `references/query-rules.md` only when you need the exact refresh and verification policy.

Use the bundled scripts instead of manually rebuilding the files:

- Create or refresh the project virtual environment with `uv sync`.
- Run `uv run scripts/collect_env.py --render-md` to collect environment facts and refresh both generated files.
- Run `uv run scripts/validate_skill.py` after editing the skill files.
- Pass `--non-interactive` when you want pure auto-detection with defaults.
- Pass `--workspace-root`, `--global-manager`, `--python-manager`, `--primary-shell`, and repeated `--note` flags when the user has already supplied those hints.

Use the project virtual environment for all skill-local operations. Do not call the scripts with a global Python interpreter unless the environment is broken and you are repairing it.

Treat the collection workflow as two layers:

1. User hints
   Capture stable conventions that automation cannot infer reliably, such as preferred workspace root, package-manager policy, Python manager policy, or warning notes for future agents.
2. Automatic detection
   Probe the local machine for shell, PATH preview, Python installations, common toolchain commands, WSL state, and Docker Desktop storage hints.

After collection:

- Treat `references/env.json` as the canonical machine-readable snapshot.
- Treat `references/environment.md` as the human-facing explanation generated from the JSON.
- Read `agent_summary` inside `env.json` before spending tokens on redundant probing.

Only inspect the live system outside the script flow if:

- the task needs verification of current state
- `env.json` is missing or stale
- the user explicitly asks to verify or update it

Prefer the recorded JSON values unless the live system contradicts them.
