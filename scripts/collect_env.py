#!/usr/bin/env python3
"""Collect local development environment facts into references/env.json."""

from __future__ import annotations

import argparse
import json
import locale
import os
import platform
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "references" / "env.json"

COMMAND_CANDIDATES = {
    "git": [["git", "--version"]],
    "uv": [["uv", "--version"]],
    "python": [["python", "--version"]],
    "python3.12": [["python3.12", "--version"]],
    "python3.10": [["python3.10", "--version"]],
    "python3.8": [["python3.8", "--version"]],
    "node": [["node", "--version"]],
    "npm": [["npm", "--version"]],
    "pnpm": [["pnpm", "--version"]],
    "yarn": [["yarn", "--version"]],
    "bun": [["bun", "--version"]],
    "go": [["go", "version"]],
    "rustc": [["rustc", "--version"]],
    "cargo": [["cargo", "--version"]],
    "docker": [["docker", "--version"]],
    "wsl": [["wsl.exe", "--version"], ["wsl.exe", "--status"]],
    "scoop": [["scoop", "--version"]],
    "winget": [["winget", "--version"]],
    "choco": [["choco", "--version"]],
}


def normalize_text(value: str) -> str:
    return value.replace("\x00", "").strip()


def decode_output(raw: bytes) -> str:
    if not raw:
        return ""
    if b"\x00" in raw:
        return raw.decode("utf-16le", errors="replace")
    for encoding in ("utf-8", locale.getpreferredencoding(False), "gbk"):
        try:
            return raw.decode(encoding)
        except UnicodeDecodeError:
            continue
    return raw.decode("utf-8", errors="replace")


def run_command(command: list[str]) -> tuple[bool, str]:
    try:
        completed = subprocess.run(
            command,
            capture_output=True,
            check=False,
        )
    except OSError as exc:
        return False, str(exc)

    output = normalize_text(decode_output(completed.stdout or completed.stderr))
    return completed.returncode == 0, output


def run_powershell(command: str) -> str:
    ok, output = run_command(["powershell.exe", "-NoProfile", "-Command", command])
    return output if ok else ""


def prompt_text(label: str, default: str | None, non_interactive: bool) -> str | None:
    if non_interactive:
        return default

    suffix = f" [{default}]" if default else ""
    raw = input(f"{label}{suffix}: ").strip()
    return raw or default


def prompt_list(label: str, default: list[str], non_interactive: bool) -> list[str]:
    if non_interactive:
        return default

    suffix = ", ".join(default)
    raw = input(f"{label} (comma separated) [{suffix}]: ").strip()
    if not raw:
        return default
    return [item.strip() for item in raw.split(",") if item.strip()]


def get_shell_name() -> str:
    if os.environ.get("POWERSHELL_DISTRIBUTION_CHANNEL") is not None:
        return "PowerShell"
    for key in ("SHELL", "ComSpec"):
        value = os.environ.get(key)
        if value:
            name = Path(value).stem
            return "PowerShell" if name.lower() in {"powershell", "pwsh"} else name
    return Path(sys.executable).stem


def detect_tool(name: str, commands: list[list[str]]) -> dict[str, Any]:
    location = shutil.which(commands[0][0])
    detected = {"name": name, "available": bool(location), "path": location, "version": None}
    if not location:
        return detected

    for command in commands:
        executable, *args = command
        invocation = build_invocation(location, args) if executable == commands[0][0] else command
        ok, output = run_command(invocation)
        if ok and output:
            detected["version"] = summarize_version(name, output)
            break
    return detected


def build_invocation(location: str, args: list[str]) -> list[str]:
    suffix = Path(location).suffix.lower()
    if suffix in {".cmd", ".bat"}:
        return ["cmd.exe", "/c", location, *args]
    return [location, *args]


def summarize_version(name: str, output: str) -> str:
    lines = [line.strip() for line in output.splitlines() if line.strip()]
    if not lines:
        return output.strip()

    if name == "wsl":
        match = re.search(r"([0-9]+\.[0-9]+\.[0-9]+(?:\.[0-9]+)?)", output)
        return f"WSL {match.group(1)}" if match else lines[0]

    if name in {"scoop", "winget"}:
        match = re.search(r"([0-9]+\.[0-9]+(?:\.[0-9]+)*)", output)
        return match.group(1) if match else ""

    for line in lines:
        if any(char.isdigit() for char in line):
            return line
    return lines[0]


def extract_python_version(version_text: str) -> str | None:
    match = re.search(r"Python\s+([0-9]+\.[0-9]+(?:\.[0-9]+)?)", version_text)
    return match.group(1) if match else None


def collect_tools() -> dict[str, Any]:
    tools = {name: detect_tool(name, commands) for name, commands in COMMAND_CANDIDATES.items()}

    python_versions = []
    for key in ("python3.8", "python3.10", "python3.12"):
        tool = tools[key]
        if tool["available"] and tool["version"]:
            version = extract_python_version(tool["version"]) or key.removeprefix("python")
            python_versions.append(version)

    return {"detected": tools, "python_versions": python_versions}


def collect_path_info() -> dict[str, Any]:
    entries = [entry for entry in os.environ.get("PATH", "").split(os.pathsep) if entry]
    return {
        "entries_preview": entries[:12],
        "preferred_python_shim": next((entry for entry in entries if ".local\\bin" in entry), None),
    }


def collect_wsl_info() -> dict[str, Any]:
    listing = run_powershell("wsl.exe --list --verbose")
    distros = []
    for raw_line in listing.splitlines():
        line = normalize_text(raw_line)
        if not line:
            continue
        cleaned = line.lstrip("*").strip()
        if not cleaned or cleaned.upper().startswith("NAME"):
            continue
        parts = re.split(r"\s{2,}", cleaned)
        if parts:
            distros.append(parts[0])
    return {"raw_listing": listing or None, "distros": distros}


def collect_docker_info() -> dict[str, Any]:
    data_root = None
    candidates = [
        Path("E:/DockerDesktop/DockerDesktopWSL"),
        Path.home() / "AppData/Local/Docker/wsl",
    ]
    for candidate in candidates:
        if candidate.exists():
            data_root = str(candidate)
            break
    return {"wsl_data_root": data_root}


def deduce_managers(tools: dict[str, Any]) -> dict[str, Any]:
    detected = tools["detected"]
    global_manager = next(
        (
            manager
            for manager in ("Scoop", "Winget", "Chocolatey")
            if detected[manager.lower() if manager != "Chocolatey" else "choco"]["available"]
        ),
        None,
    )
    python_manager = "uv" if detected["uv"]["available"] else None
    return {
        "primary_global_manager": global_manager,
        "python_manager": python_manager,
    }


def build_agent_summary(document: dict[str, Any]) -> dict[str, Any]:
    platform_info = document["platform"]
    managers = document["environment_management"]
    python = document["python"]
    notes = []

    notes.append(
        f"Machine profile: {platform_info.get('os') or 'unknown OS'}, {platform_info.get('shell') or 'unknown shell'}."
    )
    if managers.get("primary_global_manager"):
        notes.append(
            f"Prefer existing global tool manager: {managers['primary_global_manager']}."
        )
    if python.get("manager"):
        notes.append(f"Prefer {python['manager']} for Python version management.")
    if python.get("installed_versions"):
        notes.append(f"Known Python versions: {', '.join(python['installed_versions'])}.")
    if document["path"].get("preferred_python_shim"):
        notes.append(
            f"PATH should prioritize {document['path']['preferred_python_shim']} before WindowsApps."
        )

    return {
        "read_first": "Read this env.json before making machine-level assumptions.",
        "prompt_overview": " ".join(notes),
        "guardrails": [
            "Reuse the recorded managers and toolchain before introducing new global tooling.",
            "Probe the live system only when the request needs fresh verification or a machine-level change.",
            "Refresh env.json after environment changes so later agents avoid rediscovery work.",
        ],
    }


def merge_user_hints(args: argparse.Namespace, defaults: dict[str, Any]) -> dict[str, Any]:
    workspace_root = args.workspace_root or prompt_text(
        "Workspace root", defaults.get("workspace_root"), args.non_interactive
    )
    global_manager = args.global_manager or prompt_text(
        "Primary global tool manager",
        defaults.get("primary_global_manager"),
        args.non_interactive,
    )
    python_manager = args.python_manager or prompt_text(
        "Python manager", defaults.get("python_manager"), args.non_interactive
    )
    shell_name = args.primary_shell or prompt_text(
        "Primary shell", defaults.get("primary_shell"), args.non_interactive
    )
    notes = args.note or prompt_list(
        "Environment notes",
        defaults.get("notes", []),
        args.non_interactive,
    )

    return {
        "workspace_root": workspace_root,
        "primary_global_manager": global_manager,
        "python_manager": python_manager,
        "primary_shell": shell_name,
        "notes": notes,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    parser.add_argument("--workspace-root")
    parser.add_argument("--global-manager")
    parser.add_argument("--python-manager")
    parser.add_argument("--primary-shell")
    parser.add_argument("--note", action="append", default=[])
    parser.add_argument("--non-interactive", action="store_true")
    parser.add_argument("--render-md", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    tool_info = collect_tools()
    manager_defaults = deduce_managers(tool_info)

    user_hints = merge_user_hints(
        args,
        {
            "workspace_root": str(ROOT.parents[1]),
            "primary_global_manager": manager_defaults["primary_global_manager"],
            "python_manager": manager_defaults["python_manager"],
            "primary_shell": get_shell_name(),
            "notes": [],
        },
    )

    default_python = None
    if tool_info["detected"]["python"]["version"]:
        default_python = extract_python_version(tool_info["detected"]["python"]["version"])

    document = {
        "schema_version": 2,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "workspace_root": user_hints["workspace_root"],
        "platform": {
            "os": platform.system(),
            "release": platform.release(),
            "machine": platform.machine(),
            "shell": user_hints["primary_shell"] or get_shell_name(),
            "username": os.environ.get("USERNAME") or os.environ.get("USER"),
        },
        "environment_management": {
            "primary_global_manager": user_hints["primary_global_manager"],
            "notes": user_hints["notes"],
        },
        "python": {
            "manager": user_hints["python_manager"],
            "installed_versions": tool_info["python_versions"],
            "default_python": default_python,
        },
        "path": collect_path_info(),
        "wsl": collect_wsl_info(),
        "docker_desktop": collect_docker_info(),
        "tooling": tool_info["detected"],
        "user_hints": {
            "workspace_root": user_hints["workspace_root"],
            "notes": user_hints["notes"],
        },
    }
    document["agent_summary"] = build_agent_summary(document)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(document, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    if args.render_md:
        renderer = ROOT / "scripts" / "render_environment_md.py"
        subprocess.run(
            [sys.executable, str(renderer), "--input", str(output_path)],
            check=False,
        )

    print(f"Wrote {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
