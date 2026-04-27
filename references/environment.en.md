# Local Development Environment

This document is for humans. Agents should read `env.json` first.

## Snapshot

- Generated at: `2026-04-27T16:23:24.306434+00:00`
- Workspace root: `E:\VibeCoding`
- OS: `Windows 11`
- Shell: `PowerShell`
- Username: `10264`

## Manager Conventions

- Preferred global tool manager: `Scoop`
- Preferred Python manager: `uv`

## Environment Notes

- Prefer reusing existing global tools instead of introducing a new system-wide manager.
- Read env.json before making machine-level changes.

## Rules And Protected Targets

- Rules:
- None
- Protected paths:
- None
- Protected files:
- None

## Python

- Default Python: `3.12.11`
- Installed versions:
- `3.8.20`
- `3.10.20`
- `3.12.11`

## PATH

- Preferred Python shim path: `C:\Users\10264\.local\bin`
- First PATH entries:
- `C:\Users\10264\.codex\tmp\arg0\codex-arg0Dw6PXu`
- `D:\Apps\Scoop\persist\nvm\nodejs\v22.21.1\node_modules\@openai\codex\node_modules\@openai\codex-win32-x64\vendor\x86_64-pc-windows-msvc\path`
- `C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.8\bin`
- `C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.8\libnvvp`
- `C:\WINDOWS\system32`
- `C:\WINDOWS`
- `C:\WINDOWS\System32\Wbem`
- `C:\WINDOWS\System32\WindowsPowerShell\v1.0\`
- `C:\WINDOWS\System32\OpenSSH\`
- `C:\Program Files\NVIDIA Corporation\NVIDIA App\NvDLISR`
- `C:\Program Files (x86)\NVIDIA Corporation\PhysX\Common`
- `C:\Program Files\NVIDIA Corporation\Nsight Compute 2025.1.1\`

## WSL

- Known distros:
- None

## Docker Desktop

- WSL data root: `E:\DockerDesktop\DockerDesktopWSL`

## Agent Prompt Overview

- Read this env.json before making machine-level assumptions.
- Machine profile: Windows, PowerShell. Prefer existing global tool manager: Scoop. Prefer uv for Python version management. Known Python versions: 3.8.20, 3.10.20, 3.12.11. PATH should prioritize C:\Users\10264\.local\bin before WindowsApps.
- Reuse the recorded managers and toolchain before introducing new global tooling.
- Respect recorded do-not-touch paths, files, and local environment rules.
- Probe the live system only when the request needs fresh verification or a machine-level change.
- Refresh env.json after environment changes so later agents avoid rediscovery work.

## Detected Tooling

- git: git version 2.49.0.windows.1
- uv: uv 0.11.7 (9d177269e 2026-04-15 x86_64-pc-windows-msvc)
- python: C:\Users\10264\.local\bin\python.CMD
- python3.12: Python 3.12.11
- python3.10: Python 3.10.20
- python3.8: Python 3.8.20
- node: v22.21.1
- npm: 11.13.0
- docker: Docker version 29.4.0, build 9d7ad9f
- wsl: WSL 2.5.7.0
- scoop: D:\Apps\Scoop\shims\scoop.CMD
- winget: C:\Users\10264\AppData\Local\Microsoft\WindowsApps\winget.EXE
