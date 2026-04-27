#!/usr/bin/env python3
"""Render a human-readable environment summary from references/env.json."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT / "references" / "env.json"
DEFAULT_OUTPUT = ROOT / "references" / "environment.md"


def format_list(items: list[str]) -> list[str]:
    if not items:
        return ["- None"]
    return [f"- `{item}`" for item in items]


def build_markdown(env: dict) -> str:
    platform = env.get("platform", {})
    managers = env.get("environment_management", {})
    python = env.get("python", {})
    path_info = env.get("path", {})
    wsl = env.get("wsl", {})
    docker = env.get("docker_desktop", {})
    agent_summary = env.get("agent_summary", {})
    tooling = env.get("tooling", {})

    available_tools = [
        f"{name}: {details.get('version') or details.get('path')}"
        for name, details in tooling.items()
        if details.get("available")
    ]

    lines = [
        "# Local Development Environment",
        "",
        "This document is for humans. Agents should read `env.json` first.",
        "",
        "## Snapshot",
        "",
        f"- Generated at: `{env.get('generated_at_utc', 'unknown')}`",
        f"- Workspace root: `{env.get('workspace_root') or 'unknown'}`",
        f"- OS: `{platform.get('os', 'unknown')} {platform.get('release', '')}`".rstrip(),
        f"- Shell: `{platform.get('shell', 'unknown')}`",
        f"- Username: `{platform.get('username', 'unknown')}`",
        "",
        "## Manager Conventions",
        "",
        f"- Preferred global tool manager: `{managers.get('primary_global_manager') or 'unknown'}`",
        f"- Preferred Python manager: `{python.get('manager') or 'unknown'}`",
        "",
        "## Environment Notes",
        "",
    ]
    lines.extend([f"- {note}" for note in managers.get("notes", [])] or ["- None"])
    lines.extend(
        [
            "",
            "## Python",
            "",
            f"- Default Python: `{python.get('default_python') or 'unknown'}`",
            "- Installed versions:",
        ]
    )
    lines.extend(format_list(python.get("installed_versions", [])))
    lines.extend(
        [
            "",
            "## PATH",
            "",
            f"- Preferred Python shim path: `{path_info.get('preferred_python_shim') or 'unknown'}`",
            "- First PATH entries:",
        ]
    )
    lines.extend(format_list(path_info.get("entries_preview", [])))
    lines.extend(
        [
            "",
            "## WSL",
            "",
            "- Known distros:",
        ]
    )
    lines.extend(format_list(wsl.get("distros", [])))
    lines.extend(
        [
            "",
            "## Docker Desktop",
            "",
            f"- WSL data root: `{docker.get('wsl_data_root') or 'not detected'}`",
            "",
            "## Agent Prompt Overview",
            "",
            f"- {agent_summary.get('read_first', 'Read env.json first.')}",
            f"- {agent_summary.get('prompt_overview', '').strip()}",
        ]
    )
    lines.extend([f"- {item}" for item in agent_summary.get("guardrails", [])])
    lines.extend(
        [
            "",
            "## Detected Tooling",
            "",
        ]
    )
    lines.extend([f"- {tool}" for tool in available_tools] or ["- None"])
    lines.append("")
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", default=str(DEFAULT_INPUT))
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    input_path = Path(args.input)
    output_path = Path(args.output)
    env = json.loads(input_path.read_text(encoding="utf-8"))
    markdown = build_markdown(env)
    output_path.write_text(markdown, encoding="utf-8")
    print(f"Wrote {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
