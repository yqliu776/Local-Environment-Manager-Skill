# Local Development Environment

This document is for humans. Agents should read `env.json` first.

## Snapshot

- Generated at: `2026-04-28T01:03:13.225755+00:00`
- Workspace root: `<workspace-root>`
- OS: `Windows 11`
- Shell: `PowerShell`
- Username: `local-user`

## Manager Conventions

- Preferred global tool manager: `Winget`
- Preferred Python manager: `uv`

## Environment Notes

- None

## Rules And Protected Targets

- Rules:
- None
- Protected paths:
- None
- Protected files:
- None

## Python

- Default Python: `3.12.8`
- Installed versions:
- None

## PATH

- Preferred Python shim path: `unknown`
- First PATH entries:
- `%PROGRAMFILES% (x86)\PowerShell\7`
- `<redacted-path>`
- `<codex-vendor-path>`
- `%PROGRAMFILES% (x86)\Common Files\Oracle\Java\java8path`
- `%PROGRAMFILES% (x86)\Common Files\Oracle\Java\javapath`
- `%SYSTEMROOT%\system32`
- `%SYSTEMROOT%`
- `%SYSTEMROOT%\System32\Wbem`
- `%SYSTEMROOT%\System32\WindowsPowerShell\v1.0\`
- `%SYSTEMROOT%\System32\OpenSSH\`
- `%PROGRAMFILES%\dotnet\`

## WSL

- Known distros:
- None

## Docker Desktop

- WSL data root: `<docker-desktop-wsl-root>`

## Agent Prompt Overview

- Read this env.json before making machine-level assumptions.
- Machine profile: Windows, PowerShell. Prefer existing global tool manager: Winget. Prefer uv for Python version management.
- Reuse the recorded managers and toolchain before introducing new global tooling.
- Respect recorded do-not-touch paths, files, and local environment rules.
- Probe the live system only when the request needs fresh verification or a machine-level change.
- Refresh env.json after environment changes so later agents avoid rediscovery work.

## Detected Tooling

- git: git version 2.47.1.windows.2
- uv: <redacted-path>
- python: <redacted-path>
- python3.12: <redacted-path>
- python3.8: <redacted-path>
- node: v22.17.0
- npm: 11.11.0
- pnpm: 8.15.4
- docker: Docker version 28.0.1, build 068a01e
- wsl: WSL 2.4.10.0
- winget: %LOCALAPPDATA%\Microsoft\WindowsApps\winget.EXE
