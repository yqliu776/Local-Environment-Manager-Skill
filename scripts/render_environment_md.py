#!/usr/bin/env python3
"""Render bilingual human-readable environment summaries from references/env.json."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT / "references" / "env.json"
DEFAULT_OUTPUT_EN = ROOT / "references" / "environment.en.md"
DEFAULT_OUTPUT_ZH = ROOT / "references" / "environment.zh-CN.md"
LEGACY_OUTPUT = ROOT / "references" / "environment.md"

COPY = {
    "en": {
        "title": "# Local Development Environment",
        "intro": "This document is for humans. Agents should read `env.json` first.",
        "snapshot": "## Snapshot",
        "generated_at": "Generated at",
        "workspace_root": "Workspace root",
        "os": "OS",
        "shell": "Shell",
        "username": "Username",
        "manager_conventions": "## Manager Conventions",
        "global_manager": "Preferred global tool manager",
        "python_manager": "Preferred Python manager",
        "environment_notes": "## Environment Notes",
        "constraints": "## Rules And Protected Targets",
        "rules": "Rules",
        "protected_paths": "Protected paths",
        "protected_files": "Protected files",
        "python": "## Python",
        "default_python": "Default Python",
        "installed_versions": "Installed versions",
        "path": "## PATH",
        "preferred_python_shim": "Preferred Python shim path",
        "path_entries": "First PATH entries",
        "wsl": "## WSL",
        "known_distros": "Known distros",
        "docker_desktop": "## Docker Desktop",
        "wsl_data_root": "WSL data root",
        "agent_prompt_overview": "## Agent Prompt Overview",
        "detected_tooling": "## Detected Tooling",
        "none": "None",
        "unknown": "unknown",
        "not_detected": "not detected",
        "read_first": "Read this env.json before making machine-level assumptions.",
        "guardrails": [
            "Reuse the recorded managers and toolchain before introducing new global tooling.",
            "Respect recorded do-not-touch paths, files, and local environment rules.",
            "Probe the live system only when the request needs fresh verification or a machine-level change.",
            "Refresh env.json after environment changes so later agents avoid rediscovery work.",
        ],
    },
    "zh": {
        "title": "# 本地开发环境",
        "intro": "此文档面向人类阅读。Agent 应优先读取 `env.json`。",
        "snapshot": "## 快照",
        "generated_at": "生成时间",
        "workspace_root": "工作区根目录",
        "os": "操作系统",
        "shell": "Shell",
        "username": "用户名",
        "manager_conventions": "## 管理约定",
        "global_manager": "首选全局工具管理器",
        "python_manager": "首选 Python 管理器",
        "environment_notes": "## 环境备注",
        "constraints": "## 规则与受保护目标",
        "rules": "规则",
        "protected_paths": "禁止修改的目录",
        "protected_files": "禁止修改的文件",
        "python": "## Python",
        "default_python": "默认 Python",
        "installed_versions": "已安装版本",
        "path": "## PATH",
        "preferred_python_shim": "首选 Python shim 路径",
        "path_entries": "PATH 前若干项",
        "wsl": "## WSL",
        "known_distros": "已知发行版",
        "docker_desktop": "## Docker Desktop",
        "wsl_data_root": "WSL 数据根目录",
        "agent_prompt_overview": "## Agent 提示摘要",
        "detected_tooling": "## 检测到的工具",
        "none": "无",
        "unknown": "未知",
        "not_detected": "未检测到",
        "read_first": "在做机器级假设之前，请先读取此 `env.json`。",
        "guardrails": [
            "优先复用已记录的管理器和工具链，不要随意引入新的全局工具。",
            "遵守已记录的禁止修改目录、禁止修改文件和本地规则。",
            "只有在请求确实需要最新验证或涉及机器级变更时，才探测真实系统。",
            "环境发生变化后要刷新 `env.json`，避免后续 agent 重复发现同样的信息。",
        ],
    },
}

NOTE_TRANSLATIONS = {
    "Prefer reusing existing global tools instead of introducing a new system-wide manager.": "优先复用现有全局工具，不要额外引入新的系统级管理器。",
    "Read env.json before making machine-level changes.": "执行机器级变更前先读取 env.json。",
}


def format_list(items: list[str], language: str) -> list[str]:
    if not items:
        return [f"- {COPY[language]['none']}"]
    return [f"- `{item}`" for item in items]


def translate_note(note: str, language: str) -> str:
    if language == "zh":
        return NOTE_TRANSLATIONS.get(note, note)
    return note


def build_prompt_overview(env: dict, language: str) -> str:
    platform = env.get("platform", {})
    managers = env.get("environment_management", {})
    constraints = env.get("constraints", {})
    python = env.get("python", {})
    path_info = env.get("path", {})

    if language == "zh":
        parts = [
            f"机器概况：{platform.get('os', '未知系统')}，{platform.get('shell', '未知 Shell')}。",
        ]
        if managers.get("primary_global_manager"):
            parts.append(f"优先使用现有全局工具管理器：{managers['primary_global_manager']}。")
        if python.get("manager"):
            parts.append(f"Python 版本管理优先使用 {python['manager']}。")
        if python.get("installed_versions"):
            parts.append(f"已知 Python 版本：{', '.join(python['installed_versions'])}。")
        if path_info.get("preferred_python_shim"):
            parts.append(f"PATH 应优先包含 {path_info['preferred_python_shim']}，并放在 WindowsApps 之前。")
        if constraints.get("protected_paths"):
            parts.append(f"禁止修改目录：{', '.join(constraints['protected_paths'])}。")
        if constraints.get("protected_files"):
            parts.append(f"禁止修改文件：{', '.join(constraints['protected_files'])}。")
        if constraints.get("rules"):
            parts.append(f"额外规则：{'；'.join(constraints['rules'])}。")
        return "".join(parts)

    parts = [
        f"Machine profile: {platform.get('os', 'unknown OS')}, {platform.get('shell', 'unknown shell')}.",
    ]
    if managers.get("primary_global_manager"):
        parts.append(f"Prefer existing global tool manager: {managers['primary_global_manager']}.")
    if python.get("manager"):
        parts.append(f"Prefer {python['manager']} for Python version management.")
    if python.get("installed_versions"):
        parts.append(f"Known Python versions: {', '.join(python['installed_versions'])}.")
    if path_info.get("preferred_python_shim"):
        parts.append(f"PATH should prioritize {path_info['preferred_python_shim']} before WindowsApps.")
    if constraints.get("protected_paths"):
        parts.append(f"Protected paths: {', '.join(constraints['protected_paths'])}.")
    if constraints.get("protected_files"):
        parts.append(f"Protected files: {', '.join(constraints['protected_files'])}.")
    if constraints.get("rules"):
        parts.append(f"Extra rules: {'; '.join(constraints['rules'])}.")
    return " ".join(parts)


def build_markdown(env: dict, language: str) -> str:
    text = COPY[language]
    platform = env.get("platform", {})
    managers = env.get("environment_management", {})
    constraints = env.get("constraints", {})
    python = env.get("python", {})
    path_info = env.get("path", {})
    wsl = env.get("wsl", {})
    docker = env.get("docker_desktop", {})
    tooling = env.get("tooling", {})

    available_tools = [
        f"{name}: {details.get('version') or details.get('path')}"
        for name, details in tooling.items()
        if details.get("available")
    ]
    os_value = f"{platform.get('os', text['unknown'])} {platform.get('release', '')}".strip()

    lines = [
        text["title"],
        "",
        text["intro"],
        "",
        text["snapshot"],
        "",
        f"- {text['generated_at']}: `{env.get('generated_at_utc', text['unknown'])}`",
        f"- {text['workspace_root']}: `{env.get('workspace_root') or text['unknown']}`",
        f"- {text['os']}: `{os_value}`",
        f"- {text['shell']}: `{platform.get('shell', text['unknown'])}`",
        f"- {text['username']}: `{platform.get('username', text['unknown'])}`",
        "",
        text["manager_conventions"],
        "",
        f"- {text['global_manager']}: `{managers.get('primary_global_manager') or text['unknown']}`",
        f"- {text['python_manager']}: `{python.get('manager') or text['unknown']}`",
        "",
        text["environment_notes"],
        "",
    ]
    lines.extend(
        [f"- {translate_note(note, language)}" for note in managers.get("notes", [])]
        or [f"- {text['none']}"]
    )
    lines.extend(
        [
            "",
            text["constraints"],
            "",
            f"- {text['rules']}:",
        ]
    )
    lines.extend(format_list(constraints.get("rules", []), language))
    lines.extend(
        [
            f"- {text['protected_paths']}:",
        ]
    )
    lines.extend(format_list(constraints.get("protected_paths", []), language))
    lines.extend(
        [
            f"- {text['protected_files']}:",
        ]
    )
    lines.extend(format_list(constraints.get("protected_files", []), language))
    lines.extend(
        [
            "",
            text["python"],
            "",
            f"- {text['default_python']}: `{python.get('default_python') or text['unknown']}`",
            f"- {text['installed_versions']}:",
        ]
    )
    lines.extend(format_list(python.get("installed_versions", []), language))
    lines.extend(
        [
            "",
            text["path"],
            "",
            f"- {text['preferred_python_shim']}: `{path_info.get('preferred_python_shim') or text['unknown']}`",
            f"- {text['path_entries']}:",
        ]
    )
    lines.extend(format_list(path_info.get("entries_preview", []), language))
    lines.extend(
        [
            "",
            text["wsl"],
            "",
            f"- {text['known_distros']}:",
        ]
    )
    lines.extend(format_list(wsl.get("distros", []), language))
    lines.extend(
        [
            "",
            text["docker_desktop"],
            "",
            f"- {text['wsl_data_root']}: `{docker.get('wsl_data_root') or text['not_detected']}`",
            "",
            text["agent_prompt_overview"],
            "",
            f"- {text['read_first']}",
            f"- {build_prompt_overview(env, language)}",
        ]
    )
    lines.extend([f"- {item}" for item in text["guardrails"]])
    lines.extend(
        [
            "",
            text["detected_tooling"],
            "",
        ]
    )
    lines.extend([f"- {tool}" for tool in available_tools] or [f"- {text['none']}"])
    lines.append("")
    return "\n".join(lines)


def write_outputs(env: dict, output_en: Path, output_zh: Path) -> None:
    output_en.write_text(build_markdown(env, "en"), encoding="utf-8")
    output_zh.write_text(build_markdown(env, "zh"), encoding="utf-8")
    if LEGACY_OUTPUT.exists():
        LEGACY_OUTPUT.unlink()
    print(f"Wrote {output_en}")
    print(f"Wrote {output_zh}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", default=str(DEFAULT_INPUT))
    parser.add_argument("--output-en", default=str(DEFAULT_OUTPUT_EN))
    parser.add_argument("--output-zh", default=str(DEFAULT_OUTPUT_ZH))
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    input_path = Path(args.input)
    env = json.loads(input_path.read_text(encoding="utf-8"))
    write_outputs(env, Path(args.output_en), Path(args.output_zh))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
